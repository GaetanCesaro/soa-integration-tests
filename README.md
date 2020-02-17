# SOA-Integration-Tests
SOA-Integration-Tests est un utilitaire de tests d'intégration automatisés utilisant les protocoles SQL (DB2 & PostGre), REST et JMS.

<br>

## Lancement des tests
Par défaut, le lancement des tests est joué depuis [Jenkins](https://merlin-int2.intra.cafat.nc/jenkins/job/soa-integration-tests/) tous les jours aux alentours de 7h sur l'environnement de DEV. On peut également faire une exécution à la demande avec les paramètres souhaités depuis Jenkins.

### Exemples de commandes de lancement
```
py SoaIntegrationTests.py -e DEV -l DEBUG
py SoaIntegrationTests.py -e DEV -l INFO -t gpp
py SoaIntegrationTests.py -e INT -l INFO -t postgre
py SoaIntegrationTests.py -e VAL -l INFO
```

### Liste des options
| Option                              | Description                                                                                                                         |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| -h, --help                          | Aide                                                                                                                                |
| -e <environnement> (--env)          | Environnement où seront joués les tests                                                                                             |
| -t <test> (--test)                  | OPTIONNEL : Nom du ou des tests à exécuter : le terme entré est recherché dans le nom des tests référencés dans le dossier de tests |
| -l <loglevel> (--loglevel)          | OPTIONNEL : Niveau de log à appliquer à l'exécution du programme (DEBUG, INFO, WARN ou ERROR)                                       |

<br>

## Développement de nouveaux tests (utilisation locale)

### Installation Python
L'outil fonctionne en Python 3.7.

1. Installation Python 3.7 [ici](https://www.python.org/downloads/release/python-374/) ou spérieur 
1. Vérifier que la racine de l'installation Python est bien dans votre PATH (ainsi que le sous dossier Scripts)
1. Lancer la commande pip ci-dessous à la racine du repo pour récupérer les librairies nécessaires :

```
pip install -r requirements.txt
```

### Configuration ODBC 
Afin d'utiliser les connexions DB2/400, il est nécessaire de configurer une source de données ODBC sur le poste du développeur.
1. Sous Windows, aller dans *Panneau de configuration* > *Outils d'administration* > *Configurer les sources de données (ODBC)*
1. Dans l'onglet *Sources de données utilisateur*, cliquer sur *Ajouter*
1. Sélectionner le pilote **iSeries Access ODBC Driver** puis nommer la connexion **IVAL** et cliquer sur *Terminer*

### Ajout d'un nouveau test
Les fichiers de tests se trouvent dans le répertoire [tests](./tests/)
1. Dupliquer un des fichier JSON de test présent
1. Le renommer en respectant la règle de nommage ci-dessous
1. **Attention :** Bien appliquer le même nom dans la balise json *name* du fichier

### Règles de nommage des tests
La structure du nom d'un test est la suivante :

<**stack_source**>To<**stack_cible**>-<**module_source**>To<**module_cible**>-<**NomDuTestCamelEnCaseAvecMajuscule**>

Les valeurs possibles sont :
- **stack_source/stack_cible** : DB2, PostGre, JMS
- **module_source/module_cible** : gpp, cli, iam, dif, etc... 
- **NomDuTestCamelEnCaseAvecMajuscule** : CeQuonVeutTantQueCaRespecteLeCamelCaseAvecMajusculeEtPasTropLongSiPossiblePasCommeCetExempleQuoi
