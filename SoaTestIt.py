# -*- coding: utf-8 -*-
import sys, getopt
import os
import glob
import json
import src.Config as cfg
import src.Core as core
import src.Log as log
from tqdm import tqdm
from termcolor import colored


def checkParameters(env, test, loglevel):
    # Paramètres obligatoires sinon on sort
    if not env:
        log.error("L'environnement est obligatoire")  
        log.usage()
        sys.exit()

    if loglevel:
        if loglevel not in 'DEBUGINFOWARNERROR':
            log.error("Le loglevel, s'il est renseigne, doit valoir DEBUG, INFO, WARN ou ERROR")  
            log.usage()
            sys.exit()
        else:
            cfg.LOGLEVEL = loglevel


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:e:t:l:", ["help","env","test", "loglevel"])

    except getopt.GetoptError as err:
        log.error(err)  
        log.usage()
        sys.exit(2)
    
    env = ""
    test = ""
    loglevel = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            log.usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            env = arg
        elif opt in ("-t", "--test"):
            test = arg    
        elif opt in ("-l", "--loglevel"):
            loglevel = arg 
        else:
            assert False, "unhandled option"

    checkParameters(env, test, loglevel)
    

    print("ENVIRONNEMENT", env)
    ENV = cfg.ENVIRONNEMENTS[env]

    # Chargement des tests depuis les fichiers JSON
    testFilesPath = 'tests'

    results = []

    for filename in glob.glob(os.path.join(testFilesPath, '*.json')):
        # Petit saut de ligne des familles pour la clareté du log
        print("")
        log.debug("Lecture du fichier de test %s" %filename)

        with open(filename) as json_file:
            # Uniquement 1 seul test passé en paramètre de l'appel
            if test:
                if test.lower() in filename.lower():
                    data = json.load(json_file)
                    result = core.runTest(ENV, data)
                    results.append(result)
                else:
                    log.debug("--> Fichier non concerne par le filtre")
            # Tous les tests dans le dossier test
            else:
                data = json.load(json_file)
                result = core.runTest(ENV, data)
                results.append(result)

    core.exportResults(ENV, results)

    nbErrors = core.getFinalStatus(results)
    log.info("Nb errors %s" %nbErrors)

    if nbErrors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
