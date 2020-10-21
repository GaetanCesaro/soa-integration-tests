# -*- coding: utf-8 -*-

LOGLEVEL = "INFO"
GODMODE_TOKEN = "<Bearer token>"

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
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=devcompanyuser password=Devc@f@tus3r dbname=dev_company",
            "SPRINGBOOT": "https://api-dev.domain.fr",
            "JBOSS": "http://app-dev.domain.fr",
            "JMS": {
                "hostname": "http://mom-tst-01:1161",
                "broker": "ACTIVEMQ-DEV1",
            },
            "LDAP": {
                "hostname": "LDAP-DEV",
                "port": 636,
                "username": "CN=adam,DC=company,DC=fr",
                "password": "password"
            }
        }
    },
    "INT": {
        "schema_name": "INT",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=intcompanyuser password=Intc@f@tus3r dbname=int_company",
            "SPRINGBOOT": "https://api-int.domain.fr",
            "JBOSS": "http://app-int.domain.fr",
            "JMS": {
                "hostname": "http://mom-tst-01:2161",
                "broker": "ACTIVEMQ-INT",
            },
            "LDAP": {
                "hostname": "LDAP-INT",
                "port": 636,
                "username": "CN=adam,DC=company,DC=fr",
                "password": "password"
            }
        }
    },
    "VAL": {
        "schema_name": "VAL",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=valcompanyuser password=valcompanyuser dbname=val_company",
            "SPRINGBOOT": "https://api-val.domain.fr",
            "JBOSS": "http://app-val.domain.fr",
            "JMS": {
                "hostname": "http://mom-tst-01:3161",
                "broker": "ACTIVEMQ-VAL",
            },
            "LDAP": {
                "hostname": "LDAP-VAL",
                "port": 636,
                "username": "CN=adam,DC=company,DC=fr",
                "password": "password"
            }
        }
    }
}
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaIntegrationTests.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Commande", "Résultat Attendu", "Résultat Obtenu"]