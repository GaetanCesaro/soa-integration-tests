
/**
 * Pipeline build script for Services SpringBoot
 * each stage corresponds to a step in the pipeline
 */
node {

    catchError {

        properties([
            parameters(
                [
					[$class: 'ParameterSeparatorDefinition', name: 'separator_header', sectionHeader: 'Filtre de tests', sectionHeaderStyle: 'font-weight: bold; text-transform: uppercase;', separatorStyle: 'margin-top: 10px'],
					string(defaultValue: '', description: 'Nom du test à réaliser (recheche wildcard)<br/>', name: 'TEST_NAME'),
                    [$class: 'ParameterSeparatorDefinition', name: 'separator_header', sectionHeader: 'Niveau de log', sectionHeaderStyle: 'font-weight: bold; text-transform: uppercase;', separatorStyle: 'margin-top: 10px'],
                    choice(choices: 'INFO\r\nDEBUG\r\nERROR', description: 'Niveau de log', name: 'LOG_LEVEL'),
                ]
            ),
            [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', artifactDaysToKeepStr: '', artifactNumToKeepStr: '10', daysToKeepStr: '', numToKeepStr: '10']],
			pipelineTriggers([cron('H 7 * * 1-5')]),
         ])


        checkProperties()

        stage('Checkout') {
            echo "== Checkout"

            // Get code from repo
            deleteDir()
            checkout scm
        }
		
		EMAILS_A_NOTIFIER = readFile('jenkinsfile-emails.txt')

        stage('Test') {
            echo "== Test"
			
            // Récupération des dépendances
			// KO - Fait à la main sur le serveur... 
            //sh "/usr/local/bin/pip3.7 install -r requirements.txt"
            
            // Préparation de la commande shell à lancer
            shell_command = "/usr/local/bin/python3.7 SoaIntegrationTests.py -e ${env.BRANCH_NAME}"
			if(TEST_NAME) {
                shell_command = shell_command + " -t ${TEST_NAME}"
			}
            if (LOG_LEVEL) {
                shell_command = shell_command + " -l ${LOG_LEVEL}"
            }
            
            // Lancement du script Python
			sh shell_command
        }

        // At last, delete current directory to save space
        // This will only happen when the build is successful
        deleteDir()
    }
    step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: EMAILS_A_NOTIFIER, sendToIndividuals: true])
}

/**
 * The following methods are helpers used by the Build workflow above
 */

/**
 * Checks the user's choice of BUILD_MODE
 * and set build properties according to choice:
 * - $BUILD = Build, analyse and deploy to DEV/INT
 * - $RELEASE = Build, analyse, deploy to DEV/INT and Release
 *
 * If not yet set (first build), defaults to CI
 */
def checkProperties() {
    try {
		echo TEST_NAME
        echo 'TEST_NAME is defined'

        echo LOG_LEVEL
        echo 'LOG_LEVEL is defined'
    } catch (groovy.lang.MissingPropertyException ex) {
		echo 'This is the first build of the branch, TEST_NAME is not set yet. Setting it to empty.'
        TEST_NAME = ""

        echo 'This is the first build of the branch, LOG_LEVEL is not set yet. Setting it to INFO.'
        LOG_LEVEL = "INFO"
    }

    GIT_REVISION = ''

    echo "========================================"
    echo "== Test lancé sur l'environnement ${env.BRANCH_NAME} =="
    echo "========================================"

}

