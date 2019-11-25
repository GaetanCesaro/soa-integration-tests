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
import urllib3

# Disable REST InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestResult:
    def __init__(self, n="", s="", e="", g=""):
        self.testName = n
        self.status = s
        self.expectedResult = e
        self.gottenResult = g


def runSQLUpdate(environnement, test):
    server = test["in"]["server"]
    query = test["in"]["operation"]["command"]

    if server == "DB2":
        conn = pyodbc.connect(environnement["servers"][server])
    elif server == "POSTGRE":
        conn = psycopg2.connect(environnement["servers"][server])

    cursor = conn.cursor()
    log.debug("Executing %s update: %s" %(server, query))

    with conn:
        cursor.execute(query)


def runSQLCheck(environnement, test):
    server = test["out"]["server"]
    query = test["out"]["operation"]["command"]

    testResult = TestResult()
    testResult.testName = test["testName"]
    testResult.expectedResult = test["out"]["expected"]["value"]
    testResult.gottenResult = "Test check failed"
    testResult.status = "KO"

    if server == "DB2":
        conn = pyodbc.connect(environnement["servers"][server])
    elif server == "POSTGRE":
        conn = psycopg2.connect(environnement["servers"][server])

    cursor = conn.cursor()
    log.debug("Executing %s select: %s" %(server, query))

    with conn:
        cursor.execute(query)
        rows = cursor.fetchall()
        log.debug("Results: %s" %str(rows))
        
        if len(rows) > 0 and len(rows[0]) > 0:
            testResult.gottenResult = str(rows[0][0])

            if testResult.gottenResult == testResult.expectedResult:
                testResult.status = "OK"
                log.info("%s" %testResult.status)
            else:
                testResult.status = "KO"
                log.error("%s" %testResult.status)
                log.error("Expected %s" %(testResult.expectedResult))
                log.error("Gotten %s" %(testResult.gottenResult))
        else:
            testResult.gottenResult = "No result"
            testResult.status = "KO"
            log.error("%s - %s" %(testResult.status, testResult.gottenResult))

    return testResult


def runRESTPost(environnement, test):
    server = test["in"]["server"]
    url = environnement["servers"][server] + test["in"]["operation"]["command"]
    data = test["in"]["operation"]["data"]

    x = requests.post(url, json=data, verify=False)
    log.debug("Executing POST %s with data %s: %s" %(url, data, x.text))
    log.debug("Status code: %s" %(x.status_code))


def runRESTCheck(environnement, test):
    server = test["out"]["server"]
    url = environnement["servers"][server] + test["out"]["operation"]["command"]

    testResult = TestResult()
    testResult.testName = test["testName"]
    testResult.expectedResult = test["out"]["expected"]["value"]
    testResult.gottenResult = "Test check failed"
    testResult.status = "KO"

    x = requests.get(url, params=None, verify=False)
    log.debug("Executing GET %s: %s" %(url, x.text))
    log.debug("Status code: %s" %(x.status_code))
    
    if len(x.text) > 0:
        jsonResult = x.json()
        
        # Parsing de l'attribut à controler
        expectedAttribute = test["out"]["expected"]["attribute"]
        for p in expectedAttribute:
            jsonResult = jsonResult[p]

        testResult.gottenResult = jsonResult

        if testResult.gottenResult == testResult.expectedResult:
            testResult.status = "OK"
            log.info("%s" %testResult.status)
        else:
            testResult.status = "KO"
            log.error("%s" %testResult.status)
            log.error("Expected %s" %(testResult.expectedResult))
            log.error("Gotten %s" %(testResult.gottenResult))
    else:
        testResult.gottenResult = "No result"
        testResult.status = "KO"
        log.error("%s - %s" %(testResult.status, testResult.gottenResult))

    return testResult


def runTest(environnement, test):
    log.info("Running test %s" %test["testName"])

    # Modification de donnée en entrée
    if test["in"]["type"] == "SQL":
        runSQLUpdate(environnement, test)
    elif test["in"]["type"] == "REST":
        runRESTPost(environnement, test)

    # WAIT 3 s
    time.sleep(3)

    # Test en sortie
    if test["out"]["type"] == "SQL":
        result = runSQLCheck(environnement, test)
    elif test["out"]["type"] == "REST":
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
    log.info("Fichier excel cree : %s" %path)
    wb.save(path)
