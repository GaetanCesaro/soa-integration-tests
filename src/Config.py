# -*- coding: utf-8 -*-

SLEEPTIME = 8
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
    },
    "INT": {
        "name": "INT",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=intcafatuser password=Intc@f@tus3r dbname=int_cafat_01",
            "SPRINGBOOT": "https://api-int.intra.cafat.nc",
            "JBOSS": "http://app-int.intra.cafat.nc",
        }
    },
    "VAL": {
        "name": "VAL",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=valcafatuser password=valcafatuser dbname=val_cafat_01",
            "SPRINGBOOT": "https://api-val.intra.cafat.nc",
            "JBOSS": "http://app-val.intra.cafat.nc",
        }
    }
}

TESTS = [
    {
        "name": "DB2ToPostGre-MAJAdresse-Complement",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update B{envname}.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 3' where ADRCAF = '02018000007994'",
                "data": ""
            },
            "rollback_operation": {
                "command": "update B{envname}.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 2' where ADRCAF = '02018000007994'",
                "data": ""
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.gpp_adresse_domicile a inner join sgengpp.gpp_moyen_contact m on m.id = a.id_fk_ap inner join sgengpp.gpp_personne_physique p on m.fk_personne_physique = p.numero_interne where p.matricule = '540003' and m.date_fin_validite is null and a.complement = 'RES LES BAMBOUS APT 3'",
                "data": ""
            },
            "expected": {
                "attribute": "",
                "value": "1"
            }
        }
    },
    {
        "name": "DB2ToPostGre-MAJAdresse-VoieLibre",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update B{envname}.ADRESSE set ADRPA2 = 'VOIE LIBRE' where ADRCAF = '02018000007994'",
                "data": ""
            },
            "rollback_operation": {
                "command": "update B{envname}.ADRESSE set ADRPA2 = 'RUE JIM DALY' where ADRCAF = '02018000007994'",
                "data": ""
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.gpp_adresse_domicile a inner join sgengpp.gpp_moyen_contact m on m.id = a.id_fk_ap inner join sgengpp.gpp_personne_physique p on m.fk_personne_physique = p.numero_interne where p.matricule = '540003' and m.date_fin_validite is null and a.voie_libre = 'VOIE LIBRE'",
                "data": ""
            },
            "expected": {
                "attribute": "",
                "value": "1"
            }
        }
    },
    {
        "name": "PostGreToDB2-MAJAdresse-Email",
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-3.1/personne-physique/540003/contact",
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
                "command": "/s-gen-gpp-3.1/personne-physique/540003/contact",
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
                "command": "/s-gen-gpp-3.1/personne-physique/540003/contact?type=ASSURE",
                "data": ""
            },
            "expected": {
                "attribute": ["email", "adresse"],
                "value": "gaetan.cesaro+toto@gmail.com"
            }
        }
    }
]
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaTestIT.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Commande", "Résultat Attendu", "Résultat Obtenu"]