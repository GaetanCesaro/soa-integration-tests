# -*- coding: utf-8 -*-
import sys, getopt
import src.Config as cfg
import src.Core as core
import src.Log as log
from tqdm import tqdm
from termcolor import colored


def checkParameters(env, test):
    # Paramètres obligatoires sinon on sort
    if not env:
        log.error("L'environnement est obligatoire")  
        log.usage()
        sys.exit()
    #elif test:
        # TODO - Check test name connu


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:e:t:", ["help","env","test"])

    except getopt.GetoptError as err:
        log.error(err)  
        log.usage()
        sys.exit(2)
    
    env = ""
    test = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            log.usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            env = arg
        elif opt in ("-t", "--test"):
            test = arg    
        else:
            assert False, "unhandled option"

    checkParameters(env, test)

    print("ENVIRONNEMENT", env)
    ENV = cfg.ENVIRONNEMENTS[env]

    if test:
        results = []

        # Recherche de TI bien précis
        for TEST in cfg.TESTS:
             if test in TEST["name"]:
                result = core.runTest(ENV, TEST)
                results.append(result)

        core.exportResults(ENV, results)
        return core.getFinalStatus(results)

    else:
        # Tous les TI
        results = core.runAllTests(ENV)
        core.exportResults(ENV, results)
        return core.getFinalStatus(results)


if __name__ == "__main__":
    main()
