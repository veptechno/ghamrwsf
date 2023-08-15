def nsForCurrentBranch() {
    if (env.BRANCH_NAME == 'dev') {
        return 'caila-ci-dev'
    }
    if (env.BRANCH_NAME == 'stable' || env.BRANCH_NAME == 'release') {
        return 'caila-ci-stable'
    }
    return env.BRANCH_NAME
}
def myBuildResult = 'SUCCESS'
pipeline {
    options {
        gitLabConnection("gitlab just-ai")
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        disableConcurrentBuilds()
        timeout(time: 120, unit: 'MINUTES')
        timestamps()
    }
    environment {
        TRUNK_ID = "${BUILD_TIME_ID}_${BUILD_NUMBER}"
    }
    agent {
        label 'caila-dev-cloud-agent'
    }
    stages {
        stage('Build data-images') {
            steps {
                script {
                    manager.addShortText(env.BRANCH_NAME)
                }
                updateGitlabCommitStatus name: "build", state: "running"

                git url: "git@gitlab.just-ai.com:ml-platform/sd.git",
                        branch: "${env.BRANCH_NAME}",
                        credentialsId: 'bitbucket_key'

                sh """./build.sh"""
            }
        }
    }
    post {
        failure {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
        success {
            updateGitlabCommitStatus name: "build", state: "success"
        }
        unstable {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
    }
}