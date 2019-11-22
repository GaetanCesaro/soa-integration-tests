# -*- coding: utf-8 -*-

# Environnements
ENVIRONNEMENTS = {
    "LOCALHOST": {
        "name": "LOCALHOST",
        "hostname": "http://localhost:8161",
        "broker": "localhost"
    },
    "DEV": {
        "name": "DEV",
        "servers": {
            "DB2": {
                
            },
            "POSTGRE": {

            }
        },
        "broker": "ACTIVEMQ-DEV1"
    }
}

TESTS = [
    {
        "testName": "DB2-to-PostGre-MAJ-Adresse-Complement",
        "in": {
            "type": "sql",
            "server": "DB2",
            "operation": "update BDEV.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 2' where ADRCAF = '02018000007994'",
            "rollback_operation": ""
        },
        "out": {
            "type": "sql",
            "server": "POSTGRE",
            "operation": "select 1 from sgengpp.moyen_contact_view where matricule = '540003' and date_fin_validite is null and adresse_domicile like '%RES LES BAMBOUS APT 2%'",
            "expected": "toto"
        }
    },
    {
        "testName": "DB2-to-PostGre-MAJ-Adresse-Rue",
        "in": {
            "type": "sql",
            "server": "DB2",
            "operation": "update BDEV.ADRESSE set ADRPA2 = 'RUE GABRIEL LAROQUE' where ADRCAF = '02018000007994'"
        },
        "out": {
            "type": "sql",
            "server": "POSTGRE",
            "operation": "select 1 from sgengpp.moyen_contact_view where matricule = '540003' and date_fin_validite is null and adresse_domicile like '%RUE GABRIEL LAROQUE%'",
            "expected": "1"
        }
    }
]
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaTestIT.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Résultat Attendu", "Résultat Obtenu"]


# Login/Pswd
USERNAME = "admin"
PASSWORD = "admin"


# Messages processing
URL_GET_ALL_MESSAGES = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/browse()"
URL_RETRY_MESSAGES = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/retryMessages()"
#URL_GET_ONE_MESSAGE = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/browseMessages(java.lang.String)/JMSMessageID={}"
URL_POST_MESSAGE = "{}/api/jolokia/"
BODY_POST_MESSAGE = '{"type":"EXEC", "mbean":"org.apache.activemq:type=Broker,brokerName=[BROKER],destinationType=Queue,destinationName=[QUEUE]", "operation":"sendTextMessage(java.util.Map,java.lang.String,java.lang.String,java.lang.String)", "arguments":[ARGUMENTS]}'


# Queues
ALL_DLQ_QUEUES = [
    "DLQ.Consumer.SGENCLI.VirtualTopic.TDATAGPP",
    "DLQ.Consumer.SGENGPP.VirtualTopic.TDATALEGACY",
    "DLQ.QDATALEGACY",
    "DLQ.QGENCLI",
    "DLQ.QGENGPP",
    "DLQ.SGENGED",
    "DLQ.SRECDEC",
    "DLQ.SRECDNO",
    "DLQ.SRECOBL"
]
