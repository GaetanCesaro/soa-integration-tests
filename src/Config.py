# -*- coding: utf-8 -*-

LOGLEVEL = "INFO"
GODMODE_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpc3MiOiJzZWN1cmUtYXBpIiwiYXVkIjoic2VjdXJlLWFwcCIsInN1YiI6ImdvbGRAY2FmYXQubmMiLCJhY2NvdW50Ijoie1wibG9naW5cIjpcImdvbGRAY2FmYXQubmNcIixcIm1hdHJpY3VsZVwiOlwiOTk5OTk5XCIsXCJoYWJpbGl0YXRpb25zXCI6W1wiR0VORVJBTF9XX0FcIixcIk1BTEFESUVfV19BXCIsXCJSRVRSQUlURV9XX0FcIl19IiwicHJvZmlsIjoiQVNTVVJFIn0.L-yz9wzPjXkRwsSNU99Ns1Aj0POM83MI7hfz6tXssoaEnQdlVVBA-oZtuCXyQdVHW1s_d6-WhZs7ZG01LxxY3wBNvK7pmOhq1zGp-C59OUSrxMp84gP9UaeL13D6YAVnQ0AxFpyGPZowMmHvWcbjjZXNcONrVi4iZBz9IYKY0fSV1ccuw08lE_oFW2O9Orst4NCRc-RmjJF6mkzmh4oDUvRNEn-p83vn_H_wa9unu_90T6Q5vGu4n3IvkVQVkk7d_QCKD2lZzDWo0VgrdPVTc5SE_D4egUNDodZd-e7oo2ty8lY7B04_zPAEI8cXHy-54iBYEOHNqJXhUXdseHlD2g"

GPP_VERSION = "3.2"
CLI_VERSION = "2.0"
DIF_VERSION = "1.1"

JMS_USERNAME = "admin"
JMS_PASSWORD = "admin"
JMS_URL_POST_MESSAGE = "{}/api/jolokia/"
JMS_BODY_POST_MESSAGE = '{"type":"EXEC", "mbean":"org.apache.activemq:type=Broker,brokerName=[BROKER],destinationType=Topic,destinationName=[TOPIC]", "operation":"sendTextMessage(java.util.Map,java.lang.String,java.lang.String,java.lang.String)", "arguments":[ARGUMENTS]}'

ENVIRONNEMENTS = {
    "DEV": {
        "schema_name": "DEV",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=devcafatuser password=Devc@f@tus3r dbname=dev_cafat_01",
            "SPRINGBOOT": "https://api-dev.intra.cafat.nc",
            "JBOSS": "http://app-dev.intra.cafat.nc",
            "JMS": {
                "hostname": "http://mom-tst-01:1161",
                "broker": "ACTIVEMQ-DEV1",
            }
        }
    },
    "INT": {
        "schema_name": "INT",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=intcafatuser password=Intc@f@tus3r dbname=int_cafat_01",
            "SPRINGBOOT": "https://api-int.intra.cafat.nc",
            "JBOSS": "http://app-int.intra.cafat.nc",
            "JMS": {
                "hostname": "http://mom-tst-01:2161",
                "broker": "ACTIVEMQ-INT",
            }
        }
    },
    "VAL": {
        "schema_name": "VAL",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=valcafatuser password=valcafatuser dbname=val_cafat_01",
            "SPRINGBOOT": "https://api-val.intra.cafat.nc",
            "JBOSS": "http://app-val.intra.cafat.nc",
            "JMS": {
                "hostname": "http://mom-tst-01:3161",
                "broker": "ACTIVEMQ-VAL",
            }
        }
    },
    "QUA": {
        "schema_name": "GEN",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IQUA;SERVER=IVAL;DATABASE=BGEN;UID=MRECDNO;PWD=MRECDNO",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=quacafatuser password=quacafatuser dbname=qua_cafat_01",
            "SPRINGBOOT": "https://api-qua.intra.cafat.nc",
            "JBOSS": "http://app-qua.intra.cafat.nc",
            "JMS": {
                "hostname": "http://mom-tst-01:8161",
                "broker": "ACTIVEMQ-QUA",
            }
        }
    }
}
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaIntegrationTests.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Commande", "Résultat Attendu", "Résultat Obtenu"]