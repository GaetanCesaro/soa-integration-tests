# -*- coding: utf-8 -*-
import json
import os
import sys
import time

import psycopg2
import pyodbc
import requests
import urllib3
from openpyxl import Workbook
from ldap3 import Server, Connection, MODIFY_REPLACE

import src.Config as cfg
import src.Log as log

# Disable REST InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestResult:
    def __init__(self, n="", s="", e="", g=""):
        self.testName = n
        self.status = s
        self.expectedResult = e
        self.gottenResult = g


def runSQLUpdate(environnement, server, operation):
    query = operation["command"].format(SCHEMA_NAME=environnement["schema_name"])

    if server == "DB2":
        conn = pyodbc.connect(environnement["servers"][server])
    elif server == "POSTGRE":
        conn = psycopg2.connect(environnement["servers"][server])

    cursor = conn.cursor()
    log.debug("Execution %s UPDATE: %s" %(server, query))

    with conn:
        try:
            cursor.execute(query)
        except (Exception, pyodbc.Error) as e:
            log.error(str(e))


def runSQLCheck(environnement, name, check):
    server = check["server"]
    query = check["operation"]["command"].format(SCHEMA_NAME=environnement["schema_name"])

    testResult = TestResult()
    testResult.testName = name
    testResult.command = check["operation"]["command"]
    testResult.expectedResult = check["expected"]["value"]
    testResult.gottenResult = "Verification du test en echec"
    testResult.status = "KO"

    if server == "DB2":
        conn = pyodbc.connect(environnement["servers"][server])
    elif server == "POSTGRE":
        conn = psycopg2.connect(environnement["servers"][server])

    cursor = conn.cursor()
    log.debug("Execution %s SELECT: %s" %(server, query))

    with conn:
        cursor.execute(query)
        rows = cursor.fetchall()
        log.debug("Resultats: %s" %str(rows))
        
        if len(rows) > 0 and len(rows[0]) > 0:
            testResult.gottenResult = str(rows[0][0])

            if testResult.gottenResult == testResult.expectedResult:
                testResult.status = "OK"
                log.info("%s" %testResult.status)
            else:
                testResult.status = "KO"
                log.error("%s" %testResult.status)
                log.error("Attendu: %s" %(testResult.expectedResult))
                log.error("Obtenu: %s" %(testResult.gottenResult))
        else:
            if testResult.expectedResult == "":
                testResult.status = "OK"
                log.info("%s" %testResult.status)
            else:
                testResult.gottenResult = "Aucun resultat"
                testResult.status = "KO"
                log.error("%s - %s" %(testResult.status, testResult.gottenResult))

    return testResult


def runRESTPost(environnement, server, operation):
    restCommand = operation["command"].format(CLI_VERSION=cfg.CLI_VERSION, DIF_VERSION=cfg.DIF_VERSION, GPP_VERSION=cfg.GPP_VERSION)
    url = environnement["servers"][server] + restCommand
    data = operation["data"]

    try:
        response = requests.post(url, json=data, verify=False, headers={'Authorization': '{0}'.format(cfg.GODMODE_TOKEN)})

        if cfg.LOGLEVEL == 'DEBUG':
            prettyJsonData = json.dumps(data, indent=4, sort_keys=True)
            
            log.debug("Execution POST %s avec json \n%s" %(url, prettyJsonData))
            log.debug("Resultat: %s" %(response.text))
            log.debug("Status code: %s" %(response.status_code))

        if not (response.status_code >= 200 and response.status_code < 300):
            log.error("Status code: %s" %(response.status_code))

    except requests.exceptions.RequestException as e:
        log.error(str(e))


def runRESTCheck(environnement, name, check):
    server = check["server"]
    restCommand = check["operation"]["command"].format(CLI_VERSION=cfg.CLI_VERSION, DIF_VERSION=cfg.DIF_VERSION, GPP_VERSION=cfg.GPP_VERSION)
    url = environnement["servers"][server] + restCommand

    testResult = TestResult()
    testResult.testName = name
    testResult.command = check["operation"]["command"]
    testResult.expectedResult = check["expected"]["value"]
    testResult.gottenResult = "Test check failed"
    testResult.status = "KO"

    response = requests.get(url, params=None, verify=False, headers={'Authorization': '{0}'.format(cfg.GODMODE_TOKEN)})
    log.debug("Execution GET %s: %s" %(url, response.text))
    log.debug("Status code: %s" %(response.status_code))
    
    if response.ok:
        jsonResult = response.json()
        
        # Parsing de l'attribut à controler
        expectedAttribute = check["expected"]["attribute"]
        for p in expectedAttribute:
            jsonResult = jsonResult[p]

        testResult.gottenResult = jsonResult

        if testResult.gottenResult == testResult.expectedResult:
            testResult.status = "OK"
            log.info("%s" %testResult.status)
        else:
            testResult.status = "KO"
            log.error("%s" %testResult.status)
            log.error("Attendu: %s" %(testResult.expectedResult))
            log.error("Obtenu: %s" %(testResult.gottenResult))
    else:
        testResult.gottenResult = response.status_code
        testResult.status = "KO"
        log.error("%s - %s" %(testResult.status, testResult.gottenResult))

    return testResult


def runLdapUpdate(environnement, server, operation):
    dn = operation["dn"]
    fields = operation["command"]

    operations = {}

    for (field_name, field_value) in fields.items():
        operations = dict(operations, **{field_name: [(MODIFY_REPLACE, [field_value])]})

    env = environnement["servers"][server]

    server = Server(env["hostname"], env["port"], use_ssl=True)
    conn = Connection(server, env['username'], env['password'], auto_bind=True)

    conn.modify(dn, operations)

    if conn.result['result'] == 0:
        log.debug("LDAP: modif. du DN %s avec les données %s" % (dn, json.dumps(fields, indent=4, sort_keys=True)))
    else:
        log.error("LDAP: erreur modif. DN %s avec les données %s" % (dn, json.dumps(fields, indent=4, sort_keys=True)))
        log.error("Erreur: %s" % conn.last_error)

    conn.unbind()


def runLdapCheck(environnement, name, check):
    testResult = TestResult()
    testResult.testName = name
    testResult.command = check["operation"]["command"]
    testResult.expectedResult = check["expected"]["value"]
    testResult.gottenResult = ""
    testResult.status = "KO"

    env = environnement["servers"]["LDAP"]

    server = Server(env["hostname"], env["port"], use_ssl=True)
    conn = Connection(server, env['username'], env['password'], auto_bind=True)

    log.debug("Execution recherche LDAP (base: %s): %s" % (check["base"], check["operation"]["command"]))

    result = conn.search(check["base"], check["operation"]["command"])

    if result:
        log.debug("Recherche LDAP: %d résultat(s)" % (len(conn.entries)))
        if len(conn.entries) > 0:
            result_dn = conn.entries.pop().entry_dn
            testResult.gottenResult = result_dn

            if result_dn == check["expected"]["value"]:
                testResult.status = "OK"
        else:
            testResult.gottenResult = "Aucun resultat"
    elif conn.last_error is None:
        testResult.gottenResult = "Aucun resultat"
    else:
        testResult.gottenResult = conn.last_error

    if testResult.status == "OK":
        log.info(testResult.gottenResult)
    else:
        log.error("%s - %s" % (testResult.status, testResult.gottenResult))

    conn.unbind()

    return testResult


def processJMSResponse(method, response):
    if (response.status_code == 200):
        jsonResponse = json.loads(response.text)
        responseCode = jsonResponse["status"]
        log.debug("%s - HTTP Status %s" %(method, str(jsonResponse["status"])))

        if responseCode != 200:
            log.error(response.text)
            sys.exit(2)

        return jsonResponse
    else:
        log.error(method)
        log.error(response.status_code)
        log.error(response.text)


def runJMSPost(environnement, operation):
    hostname = environnement["servers"]["JMS"]["hostname"]
    broker = environnement["servers"]["JMS"]["broker"]
    topic = operation["command"]

    
    # Préparation du header JMS
    headers = operation["headers"]
    properties = "{"
    for header in headers:
        properties = properties + "\"" + header["name"] + "\":\"" + header["value"] + "\", "
    properties = properties + ", \"PersistentDelivery\":\"true\""
    properties = properties + "}"

    # Préparation du message JMS
    message = operation["data"]
    argument = []
    argument.append(properties)
    argument.append(message)
    argument.append(cfg.JMS_USERNAME)
    argument.append(cfg.JMS_PASSWORD)
    jmsMessage = json.dumps(argument)

    # Préparation de l'envoi
    textBody = cfg.JMS_BODY_POST_MESSAGE.replace("[BROKER]", broker).replace("[TOPIC]", topic).replace("[ARGUMENTS]", jmsMessage)
    log.debug(textBody)
    jsonBody = json.loads(textBody)

    # Envoi
    response = requests.post(cfg.JMS_URL_POST_MESSAGE.format(hostname), json=jsonBody, auth=(cfg.JMS_USERNAME, cfg.JMS_PASSWORD))
    return processJMSResponse("postMessage", response)


def runOperations(environment, operations):
    if type(operations) is not list:
        operations = [operations]

    for operation in operations:
        if operation["type"] == "SQL":
            runSQLUpdate(environment, operation["server"], operation["operation"])
        elif operation["type"] == "REST":
            runRESTPost(environment, operation["server"], operation["operation"])
        elif operation["type"] == "JMS":
            runJMSPost(environment, operation["operation"])
        elif operation["type"] == "LDAP":
            runLdapUpdate(environment, operation["server"], operation["operation"])
        # Si besoin, on peut spécifier un temps d'attente entre chaque opération
        if "sleeptime" in operation:
            time.sleep(operation["sleeptime"])


def runChecks(environment, name, checks):
    results = []

    if type(checks) is not list:
        checks = [checks]

    for check in checks:
        if check["type"] == "SQL":
            results.append(runSQLCheck(environment, name, check))
        elif check["type"] == "REST":
            results.append(runRESTCheck(environment, name, check))
        elif check["type"] == "LDAP":
            results.append(runLdapCheck(environment, name, check))
        # Si besoin, on peut spécifier un temps d'attente entre chaque test
        if "sleeptime" in check:
            time.sleep(check["sleeptime"])

    return results


def runTest(environnement, test):
    log.info("Lancement du test %s" % test["name"])

    # Modification de donnée en entrée
    runOperations(environnement, test["in"])

    # WAIT
    time.sleep(test["sleeptime"])

    # Tests en sortie
    results = runChecks(environnement, test["name"], test["out"])

    # Rollback operation faite en entrée
    runOperations(environnement, test["rollback"])

    # WAIT SINON CA PEUT IMPACTER LES TESTS SUIVANTS
    time.sleep(test["sleeptime"])

    return results


def exportResults(envName, results):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "SoaIntegrationTests - Resultats"
    ws1.append(cfg.EXCEL_COLUMNS)

    for result in results:
        ws1.append([result.testName, result.status, result.command, result.expectedResult, result.gottenResult])

    pathFolder = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-4] + '\\' + cfg.OUTPUT_FOLDER
    if not os.path.exists(pathFolder):
        os.mkdir(pathFolder)

    path = pathFolder + envName + cfg.EXCEL_FILE_NAME
    log.info("Fichier excel cree : %s" %path)
    wb.save(path)


def getFinalStatus(results):
    errors = 0

    for result in results:
        if result.status != "OK":
            errors = errors + 1
    
    return errors
