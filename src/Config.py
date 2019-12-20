# -*- coding: utf-8 -*-

LOGLEVEL = "INFO"
GODMODE_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJpc3MiOiJzZWN1cmUtYXBpIiwiYXVkIjoic2VjdXJlLWFwcCIsInN1YiI6ImdvbGRAY2FmYXQubmMiLCJhY2NvdW50Ijoie1wibG9naW5cIjpcImdvbGRAY2FmYXQubmNcIixcIm1hdHJpY3VsZVwiOlwiOTk5OTk5XCIsXCJoYWJpbGl0YXRpb25zXCI6W1wiR0VORVJBTF9XX0FcIixcIk1BTEFESUVfV19BXCIsXCJSRVRSQUlURV9XX0FcIl19IiwicHJvZmlsIjoiQVNTVVJFIn0.L-yz9wzPjXkRwsSNU99Ns1Aj0POM83MI7hfz6tXssoaEnQdlVVBA-oZtuCXyQdVHW1s_d6-WhZs7ZG01LxxY3wBNvK7pmOhq1zGp-C59OUSrxMp84gP9UaeL13D6YAVnQ0AxFpyGPZowMmHvWcbjjZXNcONrVi4iZBz9IYKY0fSV1ccuw08lE_oFW2O9Orst4NCRc-RmjJF6mkzmh4oDUvRNEn-p83vn_H_wa9unu_90T6Q5vGu4n3IvkVQVkk7d_QCKD2lZzDWo0VgrdPVTc5SE_D4egUNDodZd-e7oo2ty8lY7B04_zPAEI8cXHy-54iBYEOHNqJXhUXdseHlD2g"

GPP_VERSION = "3.2"
CLI_VERSION = "2.0"

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
        "name": "PostGreToPostGre-GppToGpp-Email",
        "sleeptime": 3,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro+test@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact?type=ASSURE",
                "data": ""
            },
            "expected": {
                "attribute": ["email", "adresse"],
                "value": "gaetan.cesaro+test@gmail.com"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "DB2ToPostGre-MAJAdresse-Complement",
        "sleeptime": 3,
        "in": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update B{envname}.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 3' where ADRCAF = '02018000007994'",
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
        },
        "rollback": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "update B{envname}.ADRESSE set ADRPA1 = 'RES LES BAMBOUS APT 2' where ADRCAF = '02018000007994'",
                "data": ""
            }
        }
    },
    {
        "name": "PostGreToDB2-MAJAdresse-Email",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro+test@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "DB2",
            "operation": {
                "command": "select 1 from B{envname}.ADRESSE where ADRCAF = '02018000007994' and ADREML = 'gaetan.cesaro+test@gmail.com'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-GppToCli-Email",
        "sleeptime": 4,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro+test@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact a inner join sgencli.cli_client c on c.id = a.id_fk_client inner join sgencli.cli_personne_physique p on p.id_fk_client = c.id where p.matricule = 540003 and a.email like 'gaetan.cesaro+test@gmail.com%'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "email": {
                        "type": "email",
                        "typeContact": "ASSURE",
                        "adresse": "gaetan.cesaro@gmail.com"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-GppToCli-TelephoneMobile",
        "sleeptime": 4,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "telephoneMobile": {
                        "type": "mobile",
                        "typeContact": "ASSURE",
                        "numero": "123456"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact a inner join sgencli.cli_client c on c.id = a.id_fk_client inner join sgencli.cli_personne_physique p on p.id_fk_client = c.id where p.matricule = 540003 and a.telephone_mobile like '123456%'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "telephoneMobile": {
                        "type": "mobile",
                        "typeContact": "ASSURE",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-GppToCli-TelephoneFixe",
        "sleeptime": 4,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "telephoneFixe": {
                        "type": "fixe",
                        "typeContact": "ASSURE",
                        "numero": "123456"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact a inner join sgencli.cli_client c on c.id = a.id_fk_client inner join sgencli.cli_personne_physique p on p.id_fk_client = c.id where p.matricule = 540003 and a.telephone_fixe like '123456%'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "telephoneFixe": {
                        "type": "fixe",
                        "typeContact": "ASSURE",
                        "numero": "0"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-GppToCli-AdressePostale",
        "sleeptime": 6, 
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
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
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "libre",
                            "numero": "15",
                            "libelle": "VOIE LIBRE"
                        }
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact a inner join sgencli.cli_client c on c.id = a.id_fk_client inner join sgencli.cli_personne_physique p on p.id_fk_client = c.id where p.matricule = 540003 and a.adresse_postale like '%VOIE LIBRE%'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-gpp-"+GPP_VERSION+"/personne-physique/540003/contact",
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
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToCli-TelephoneFixe",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "123456"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact c, sgencli.cli_personne_physique pp where c.id_fk_client = pp.id_fk_client and pp.matricule = '540003' and c.telephone_fixe = '123456'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToGpp-TelephoneFixe",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "123456"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.gpp_telephone_fixe t, sgengpp.gpp_moyen_contact mc, sgengpp.gpp_personne_physique pp where t.id_fk_moyen_contact = mc.id and mc.date_fin_validite is null and mc.fk_personne_physique = pp.numero_interne and pp.matricule = 540003 and t.numero = '123456'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToCli-TelephoneMobile",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "123456"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact c, sgencli.cli_personne_physique pp where c.id_fk_client = pp.id_fk_client and pp.matricule = '540003' and c.telephone_mobile = '123456'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToGpp-TelephoneMobile",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "123456"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.gpp_telephone_mobile t, sgengpp.gpp_moyen_contact mc, sgengpp.gpp_personne_physique pp where t.id_fk_moyen_contact = mc.id and mc.date_fin_validite is null and mc.fk_personne_physique = pp.numero_interne and pp.matricule = 540003 and t.numero = '123456'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToCli-AdressePostale",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "28871"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES CITRONS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "TRIANON"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "16",
                            "id": 502250
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgencli.cli_contact c, sgencli.cli_personne_physique pp where c.id_fk_client = pp.id_fk_client and pp.matricule = '540003' and c.adresse_postale like '%CITRONS%16,%HENDRIX%TRIANON%98809 %DORE%'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToGpp-AdressePostale",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "28871"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES CITRONS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "TRIANON"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "16",
                            "id": 502250
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgengpp.gpp_adresse_domicile ad, sgengpp.gpp_moyen_contact mc, sgengpp.gpp_personne_physique pp where ad.id_fk_ap = mc.id and mc.date_fin_validite is null and mc.fk_personne_physique = pp.numero_interne and pp.matricule = 540003 and ad.complement like '%CITRONS%' and ad.fk_voie = 502250 and ad.lieu_dit_libre = 'TRIANON' and numero_voie = '16'",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/contact",
                "data": {
                    "adressePostale": {
                        "type": "domicile",
                        "ligneDesserte": {
                            "type": "reference",
                            "id": "6833"
                        },
                        "lignePays": {
                            "code": "540"
                        },
                        "ligneComplement": "RES LES BAMBOUS APT 3",
                        "ligneLieuDit": {
                            "type": "libre",
                            "libelle": "VAL PLAISANCE"
                        },
                        "ligneVoie": {
                            "type": "reference",
                            "numero": "15",
                            "id": 502249
                        }
                    },
                    "telephoneFixe": {
                        "type": "fixe",
                        "numero": "0"
                    },
                    "telephoneMobile": {
                        "type": "mobile",
                        "numero": "522933"
                    },
                    "typeContact": "ASSURE"
                }
            }
        }
    },
    {
        "name": "PostGreToPostGre-CliToDif-PreferencesNotifications",
        "sleeptime": 6,
        "in": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/preferences-notifications",
                "data": {
                    "abonnementEmail": "true",
                    "abonnementSms": "true"
                }
            }
        },
        "out": {
            "type": "SQL",
            "server": "POSTGRE",
            "operation": {
                "command": "select 1 from sgendif.dif_preferences_notifications where numero_assure = '540003' and abonnement_email = true and abonnement_sms = true",
                "data": ""
            },
            "expected": {
                "attribute": "1",
                "value": "1"
            }
        },
        "rollback": {
            "type": "REST",
            "server": "SPRINGBOOT",
            "operation": {
                "command": "/s-gen-cli-"+CLI_VERSION+"/personne-physique/540003/preferences-notifications",
                "data": {
                    "abonnementEmail": "false",
                    "abonnementSms": "false"
                }
            }
        }
    }
]
    
# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_SoaTestIT.xlsx"
EXCEL_COLUMNS = ["Nom du test", "Statut", "Commande", "Résultat Attendu", "Résultat Obtenu"]