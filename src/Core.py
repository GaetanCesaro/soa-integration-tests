# -*- coding: utf-8 -*-
import pyodbc
import psycopg2
import time
import requests
import json
import difflib
import csv
import re
import os
import time
from tqdm import tqdm
import sys, getopt
from openpyxl import Workbook
import src.Config as cfg
import src.Log as log

class TestResult:
    def __init__(self, n="", s="", e="", g=""):
        self.testName = n
        self.status = s
        self.expectedResult = e
        self.gottenResult = g


def runSQLUpdate(environnement, test):
    databaseType = test["in"]["server"]
    query = test["in"]["operation"]

    if databaseType == "DB2":
        conn = pyodbc.connect('DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST')
    elif databaseType == "POSTGRE":
        conn = psycopg2.connect(user="devcafatuser", password="Devc@f@tus3r", host="dbpg-qua-80", port="5432", database="dev_cafat_01")

    cursor = conn.cursor()
    #log.ok("Executing %s update: %s" %(databaseType, query))

    with conn:
        cursor.execute(query)


def runSQLCheck(environnement, test):
    databaseType = test["out"]["server"]
    query = test["out"]["operation"]

    testResult = TestResult()
    testResult.testName = test["testName"]
    testResult.expectedResult = test["out"]["expected"]
    testResult.gottenResult = "Test check failed"
    testResult.status = "KO"

    if databaseType == "DB2":
        conn = pyodbc.connect('DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST')
    elif databaseType == "POSTGRE":
        conn = psycopg2.connect(user="devcafatuser", password="Devc@f@tus3r", host="dbpg-qua-80", port="5432", database="dev_cafat_01")

    cursor = conn.cursor()
    #log.ok("Executing %s select: %s" %(databaseType, query))

    with conn:
        cursor.execute(query)
        rows = cursor.fetchall()
        #log.ok("Results: %s" %str(rows))
        
        if len(rows) > 0 and len(rows[0]) > 0:
            testResult.gottenResult = str(rows[0][0])
            #log.ok("Expected %s, Gotten %s" %(testResult.gottenResult, testResult.expectedResult))

            if testResult.gottenResult == testResult.expectedResult:
                testResult.status = "OK"
                log.ok("%s" %testResult.status)
            else:
                testResult.status = "KO"
                log.error("%s" %testResult.status)
        else:
            testResult.gottenResult = "No result"
            testResult.status = "KO"
            log.error("%s" %testResult.status)

    return testResult


def runRESTPost(environnement, test):
    databaseType = test["in"]["server"]
    query = test["in"]["operation"]

    if databaseType == "DB2":
        conn = pyodbc.connect('DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST')
    elif databaseType == "POSTGRE":
        conn = psycopg2.connect(user="devcafatuser", password="Devc@f@tus3r", host="dbpg-qua-80", port="5432", database="dev_cafat_01")

    cursor = conn.cursor()
    #log.ok("Executing %s update: %s" %(databaseType, query))

    with conn:
        cursor.execute(query)


def runRESTCheck(environnement, test):
    databaseType = test["out"]["server"]
    query = test["out"]["operation"]

    testResult = TestResult()
    testResult.testName = test["testName"]
    testResult.expectedResult = test["out"]["expected"]
    testResult.gottenResult = "Test check failed"
    testResult.status = "KO"

    if databaseType == "DB2":
        conn = pyodbc.connect('DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST')
    elif databaseType == "POSTGRE":
        conn = psycopg2.connect(user="devcafatuser", password="Devc@f@tus3r", host="dbpg-qua-80", port="5432", database="dev_cafat_01")

    cursor = conn.cursor()
    #log.ok("Executing %s select: %s" %(databaseType, query))

    with conn:
        cursor.execute(query)
        rows = cursor.fetchall()
        #log.ok("Results: %s" %str(rows))
        
        if len(rows) > 0 and len(rows[0]) > 0:
            testResult.gottenResult = str(rows[0][0])
            #log.ok("Expected %s, Gotten %s" %(testResult.gottenResult, testResult.expectedResult))

            if testResult.gottenResult == testResult.expectedResult:
                testResult.status = "OK"
                log.ok("%s" %testResult.status)
            else:
                testResult.status = "KO"
                log.error("%s" %testResult.status)
        else:
            testResult.gottenResult = "No result"
            testResult.status = "KO"
            log.error("%s" %testResult.status)

    return testResult


def runTest(environnement, test):
    log.ok("Running test %s" %test["testName"])

    # Modification de donnée en entrée
    if test["type"] == "sql":
        runSQLUpdate(environnement, test)
    elif test["type"] == "rest":
        runRESTPost(environnement, test)

    # WAIT 3 s
    time.sleep(3)

    # Test en sortie
    if test["type"] == "sql":
        result = runSQLCheck(environnement, test)
    elif test["type"] == "rest":
        result = runRESTCheck(environnement, test)

    return result


def runAllTests(environnement):
    results = []
    
    for test in cfg.TESTS:
        result = runTest(environnement, test)
        results.append(result)
        
    return results


def exportResults(environnement, results):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "SoaTestIT - Results"
    ws1.append(cfg.EXCEL_COLUMNS)

    for result in results:
        ws1.append([result.testName, result.status, result.expectedResult, result.gottenResult])

    pathFolder = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-4] + '\\' + cfg.OUTPUT_FOLDER
    if not os.path.exists(pathFolder):
        os.mkdir(pathFolder)

    path = pathFolder + environnement["name"] + cfg.EXCEL_FILE_NAME
    log.ok("Fichier excel cree : %s" %path)
    wb.save(path)


###########################################################################################################################

def processJsonResponse(method, response):
    if (response.status_code == 200):
        jsonResponse = json.loads(response.text)
        responseCode = jsonResponse["status"]
        log.ok("%s - HTTP Status %s" %(method, str(jsonResponse["status"])))

        if responseCode != 200:
            log.error(response.text)
            sys.exit(2)

        return jsonResponse
    else:
        log.error(method)
        log.error(response)


def getAllMessages(environnement, queue):
    response = requests.get(cfg.URL_GET_ALL_MESSAGES.format(environnement["hostname"], environnement["broker"], queue), params=None, verify=False, auth=(cfg.USERNAME, cfg.PASSWORD))
    return processJsonResponse("getAllMessages", response)


def formatMessages(jsonResponse, environnement, queue, writeExcelFile):
    messageList = []
    if writeExcelFile:    
        wb = Workbook()
        ws1 = wb.active
        ws1.title = queue[0 : 31]
        ws1.append(cfg.EXCEL_COLUMNS[queue])

        #ws2 = wb.create_sheet(title="TEST2")

    if not jsonResponse["value"]:
        log.error("Rien a formater")
        sys.exit(2)

    for message in tqdm(jsonResponse["value"], desc="formatMessages"):
        
        #properties = json.dumps(message["StringProperties"]).replace("u'", "'")
        properties = "{"
        headers = message["StringProperties"]
        for header in headers:
            if header != 'dlqDeliveryFailureCause':
                properties = properties + "\"" + header + "\":\"" + message["StringProperties"][header] + "\", "

        properties = properties + "\"JMSDeliveryMode\":\"" + message["JMSDeliveryMode"] + "\""
        properties = properties + ", \"JMSPriority\":\"" + str(message["JMSPriority"]) + "\""
        properties = properties + "}"

        # 1ere passe de formatage
        text = json.dumps(message["Text"]).replace(' ', '').replace('\\\"', '"')

        # ajout dans le fichier excel
        if writeExcelFile: 
            dlqDeliveryFailureCause = message["StringProperties"]['dlqDeliveryFailureCause']

            if queue == "DLQ.Consumer.SGENGPP.VirtualTopic.TDATALEGACY":
                table = message["StringProperties"]['TABLE']
                operation = message["StringProperties"]['OPERATION']
                ws1.append([table, operation, dlqDeliveryFailureCause, properties, text.replace('\\\"', '"').replace('"{"', '{"').replace('"}"', '"}')])
            else:
                ws1.append([dlqDeliveryFailureCause, properties, text.replace('\\\"', '"').replace('"{"', '{"').replace('"}"', '"}')])
            

        argument = []
        argument.append(properties)
        argument.append(text)
        argument.append(cfg.USERNAME)
        argument.append(cfg.PASSWORD)

        # 2eme passe de formatage pour préparer le body
        argumentText = json.dumps(argument).replace('\\\"', '"').replace('\\\"', '"').replace('\\\"', '"').replace('\\\"', '"').replace('"{"', '{"').replace('"{"', '{"').replace('"}"', '"}').replace('"}"', '"}').replace('}"",', '},')
        messageList.append(argumentText)

    if writeExcelFile:
        pathFolder = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-4] + '\\' + cfg.OUTPUT_FOLDER
        if not os.path.exists(pathFolder):
            os.mkdir(pathFolder)
        path = pathFolder + environnement["name"] + cfg.EXCEL_FILE_NAME
        log.ok("fichier excel: %s" %path)
        wb.save(path)
    
    time.sleep(0.1)
    log.ok("formatMessages - {} messages traites".format(len(messageList)))
    return messageList


def postMessage(environnement, queue, message):
    if(environnement["name"] == "PRD" or environnement["hostname"] == "http://mom-prd-01:8161"):
        log.error("postMessage - Environnement PRD interdit")
        return

    textBody = cfg.BODY_POST_MESSAGE.replace("[BROKER]", environnement["broker"]).replace("[QUEUE]", queue).replace("[ARGUMENTS]", message)
    jsonBody = json.loads(textBody)

    response = requests.post(cfg.URL_POST_MESSAGE.format(environnement["hostname"]), json=jsonBody, auth=(cfg.USERNAME, cfg.PASSWORD))
    return processJsonResponse("postMessage", response)


def retryMessages(environnement, queue):
    response = requests.get(cfg.URL_RETRY_MESSAGES.format(environnement["hostname"], environnement["broker"], queue), params=None, verify=False, auth=(cfg.USERNAME, cfg.PASSWORD))
    jsonResponse = processJsonResponse("retryMessages", response)

    if jsonResponse:
        log.ok("Queue %s - Nb message rejoues: %s" %(queue, str(jsonResponse["value"])))
        return jsonResponse

