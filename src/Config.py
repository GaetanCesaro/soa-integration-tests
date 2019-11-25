# -*- coding: utf-8 -*-

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
        "testName": "PostGre-to-DB2-MAJ-Adresse",
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": "/s-gen-gpp-3.2/personne-physique/540003/contact",
            "data": {
                "email": {
                    "type": "email",
                    "typeContact": "ASSURE",
                    "adresse": "gaetan.cesaro+titi@gmail.com"
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
            "expected": "gaetan.cesaro+titi@gmail.com"
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