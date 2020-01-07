
/**
 * Pipeline build script for Services SpringBoot
 * each stage corresponds to a step in the pipeline
 */
node {

    catchError {

        properties([
            parameters(
                [
                    [$class: 'ParameterSeparatorDefinition', name: 'separator_header', sectionHeader: 'Environnement', sectionHeaderStyle: 'font-weight: bold; text-transform: uppercase;', separatorStyle: 'margin-top: 10px'],
                    choice(choices: 'DEV\r\nINT\r\nVAL', description: '''Choix de l\'environnement cible<br/>''', name: 'DEPLOY_ENV_TARGET'),
					[$class: 'ParameterSeparatorDefinition', name: 'separator_header', sectionHeader: 'Filtre de tests', sectionHeaderStyle: 'font-weight: bold; text-transform: uppercase;', separatorStyle: 'margin-top: 10px'],
					string(defaultValue: '', description: 'Nom du test à réaliser (recheche wildcard)', name: 'TEST_NAME'),
                ]
             ),
             [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', artifactDaysToKeepStr: '', artifactNumToKeepStr: '10', daysToKeepStr: '', numToKeepStr: '10']],
         ])


        checkProperties()

        stage('Checkout') {
            echo "== Checkout"

            // Get code from repo
            deleteDir()
            checkout scm

            // Start build status
            GIT_REVISION = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
            sh "curl --insecure -H 'Authorization: Bearer ${env.BUILD_STATUS_BITBUCKET_TOKEN}' " +
                "-H 'X-Atlassian-Token: no-check' " +
                "-H 'Content-Type: application/json' " +
                "-X POST " +
                "-d '{\"state\": \"INPROGRESS\", \"key\": \"${env.JOB_NAME}\", \"name\": \"${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME}\", \"url\": \"${env.RUN_DISPLAY_URL}\"}' " +
                "${env.BITBUCKET_BASE_URL}/rest/build-status/1.0/commits/${GIT_REVISION}"
        }

        stage('Test') {
            echo "== Test"

            // Run the python script
			if(TEST_NAME) {
				sh "python3.7 -e ${DEPLOY_ENV_TARGET} -t ${TEST_NAME}"
			} else {
				sh "python3.7 -e ${DEPLOY_ENV_TARGET}"
			}
        }

        // At last, delete current directory to save space
        // This will only happen when the build is successful
        deleteDir()

        // Finalize build status
        sh "curl --insecure -H 'Authorization: Bearer ${env.BUILD_STATUS_BITBUCKET_TOKEN}' " +
            "-H 'X-Atlassian-Token: no-check' " +
            "-H 'Content-Type: application/json' " +
            "-X POST " +
            "-d '{\"state\": \"SUCCESSFUL\", \"key\": \"${env.JOB_NAME}\", \"name\": \"${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME}\", \"url\": \"${env.RUN_DISPLAY_URL}\"}' " +
            "${env.BITBUCKET_BASE_URL}/rest/build-status/1.0/commits/${GIT_REVISION}"
    }
    step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: emailextrecipients([[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider'], [$class: 'CulpritsRecipientProvider']])])

    if (GIT_REVISION && currentBuild.result.equals("FAILURE")) {
        sh "curl --insecure -H 'Authorization: Bearer ${env.BUILD_STATUS_BITBUCKET_TOKEN}' " +
            "-H 'X-Atlassian-Token: no-check' " +
            "-H 'Content-Type: application/json' " +
            "-X POST " +
            "-d '{\"state\": \"FAILED\", \"key\": \"${env.JOB_NAME}\", \"name\": \"${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME}\", \"url\": \"${env.RUN_DISPLAY_URL}\"}' " +
            "${env.BITBUCKET_BASE_URL}/rest/build-status/1.0/commits/${GIT_REVISION}"
    }
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
        echo DEPLOY_ENV_TARGET
        echo 'DEPLOY_ENV_TARGET is defined'
    } catch (groovy.lang.MissingPropertyException ex) {
        echo 'This is the first build of the branch, DEPLOY_ENV_TARGET is not set yet. Setting it to DEV.'
        DEPLOY_ENV_TARGET = "DEV"
    }

    GIT_REVISION = ''

    echo "========================================================="
    echo "== Test lancé sur l'environnement ${DEPLOY_ENV_TARGET} =="
    echo "========================================================="

}

