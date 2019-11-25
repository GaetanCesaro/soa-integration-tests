# -*- coding: utf-8 -*-

LOGLEVEL = "INFO"

ENVIRONNEMENTS = {
    "DEV": {
        "name": "DEV",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=IVAL;SERVER=IVAL;DATABASE=BGEN;UID=INFTEST;PWD=INFTEST",
            "POSTGRE": "host=dbpg-qua-80 port=5432 user=devcafatuser password=Devc@f@tus3r database=dev_cafat_01",
            "SPRINGBOOT": "https://api-dev.intra.cafat.nc",
            "JBOSS": "http://app-dev.intra.cafat.nc",
        }
    }
}

TESTS = [
    {
        "testName": "PostGre-to-DB2-MAJ-Adresse",
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": "/s-gen-gpp-3.2/personne-physique/540003/contact",
            "data": {
                "adressePostale": {
                    "type": "domicile",
                    "typeContact": "ASSURE",
                    "ligneDesserte": {
                        "type": "reference",
                        "id": 6833
                    },
                    "lignePays": {
                        "code": "540"
                    },
                    "ligneComplement": "RES LES BAMBOUS APT 2",
                    "ligneLieuDit": {
                        "type": "libre",
                        "libelle": "VAL PLAISANCE"
                    },
                    "ligneVoie": {
                        "type": "reference",
                        "numero": "15",
                        "id": 422958
                    }
                },
                "adresseFormattee": "RES LES BAMBOUS APT 2\n15, RUE GABRIEL LAROQUE\nVAL PLAISANCE\n98800 NOUMEA\nNOUVELLE-CALEDONIE",
                "email": {
                    "type": "email",
                    "typeContact": "ASSURE",
                    "adresse": "gaetan.cesaro+coucou@gmail.com"
                },
                "telephoneFixe": {
                    "type": "fixe",
                    "typeContact": "ASSURE",
                    "numero": "0"
                },
                "telephoneMobile": {
                    "type": "mobile",
                    "typeContact": "ASSURE",
                    "numero": "522933"
                },
                "typeContact": "ASSURE"
            },
            "rollback_operation": ""
        },
        "out": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": "/s-gen-gpp-3.2/personne-physique/540003/contact?type=ASSURE",
            "expectedAttribute": ["email", "adresse"],
            "expected": "gaetan.cesaro+coucou@gmail.com"
        }
    },
    {
        "testName": "DB2-to-PostGre-MAJ-Adresse-Complement",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": "update BDEV.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 2' where ADRCAF = '02018000007994'",
            "rollback_operation": ""
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": "select 1 from sgengpp.moyen_contact_view where matricule = '540003' and date_fin_validite is null and adresse_domicile like '%RES LES BAMBOUS APT 2%'",
            "expected": "1"
        }
    },
    {
        "testName": "DB2-to-PostGre-MAJ-Adresse-Rue",
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": "update BDEV.ADRESSE set ADRPA2 = 'RUE GABRIEL LAROQUE' where ADRCAF = '02018000007994'"
        },
        "out": {
            "type": "SQL",
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