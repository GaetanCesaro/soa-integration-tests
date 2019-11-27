# -*- coding: utf-8 -*-
from tqdm import tqdm
from termcolor import colored
import src.Config as cfg


# Logs tqdm configuration
def debug(msg): 
    if cfg.LOGLEVEL == "DEBUG":
        tqdm.write(colored('[DEBUG] ' + msg, 'yellow'))

def info(msg): tqdm.write(colored('[INFO] ' + msg, 'green'))
def warn(msg): tqdm.write(colored('[WARN] ' + 'orange'))
def error(msg): tqdm.write(colored('[ERROR] --> ' + msg, 'red'))

# Usage
def usage():
    print("Utilisation : ")
    print("python SoaTestIt.py -e <environnement> -t <test>")
    print("")
    print("Options : ")
    print("-e <environnement> (--env) : Environnement où seront joués les tests")
    print("-t <test> (--test) OPTIONNEL : Nom du ou des tests a éxécuter : le terme entré est recherché dans le nom des tests référencés.")
    print("---")
    print("  Actions possibles : postFirstMessage, postAllMessages, retryMessages, retryMessagesAllQueues, exportExcel (voir README.md)")
    print("  Environnements possibles : DEV, INT, VAL")
    print("  Exemples de tests à rechecher : PostGreToDB2, DB2ToPostGre, PostGreToPostGre, ...")
    print("  Exemples: python SoaTestIt.py -e INT -t PostGreToDB2")
    print("            python SoaTestIt.py -e VAL")
    print("---")