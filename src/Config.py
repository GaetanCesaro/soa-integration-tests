# -*- coding: utf-8 -*-

SLEEPTIME = 10
LOGLEVEL = "INFO"

ENVIRONNEMENTS = {
    "DEV": {
        "name": "DEV",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=devcafatuser password=Devc@f@tus3r dbname=dev_cafat_01",
            "SPRINGBOOT": "https://api-dev.intra.cafat.nc",
            "JBOSS": "http://app-dev.intra.cafat.nc",
        }
    }
}

TESTS = [
    {
        "testName": "PostGreToDB2-MAJAdresse-Email",
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-3.2/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro+toto@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            },
            "rollback_operation": {
                "command": "/s-gen-gpp-3.2/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-3.2/personne-physique/540003/contact?type=ASSURE",
                "data": ""
            },
            "expected": {
                "attribute": ["email", "adresse"],
                "value": "gaetan.cesaro+toto@gmail.com"
            }
        }
    },
    {
        "testName": "DB2ToPostGre-MAJAdresse-Complement",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update BDEV.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 3' where ADRCAF = '02018000007994'",
                "data": ""
            },
            "rollback_operation": {
                "command": "update BDEV.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 2' where ADRCAF = '02018000007994'",
                "data": ""
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.moyen_contact_view where matricule = '540003' and date_fin_validite is null and adresse_domicile like '%RES LES BAMBOUS APT 3%'",
                "data": ""
            },
            "expected": {
                "attribute": "",
                "value": "1"
            }
        }
    },
    {
        "testName": "DB2ToPostGre-MAJAdresse-Rue",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update BDEV.ADRESSE set ADRPA2 = 'RUE GABRIEL LAROQUE' where ADRCAF = '02018000007994'",
                "data": ""
            },
            "rollback_operation": {
                "command": "update BDEV.ADRESSE set ADRPA2 = 'RUE JIM DALY' where ADRCAF = '02018000007994'",
                "data": ""
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.moyen_contact_view where matricule = '540003' and date_fin_validite is null and adresse_domicile like '%RUE GABRIEL LAROQUE%'",
                "data": ""
            },
            "expected": {
                "attribute": "",
                "value": "1"
            }
        }
    }
]
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaTestIT.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Commande", "Résultat Attendu", "Résultat Obtenu"]