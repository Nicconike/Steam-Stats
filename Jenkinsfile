pipeline {
    agent {
        label 'windows-local'
    }
    options {
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }
    environment {
        PYTHON = 'python3'
        VENV_DIR = 'jenkins_venv'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/jenkins-experiment']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Nicconike/Steam-Stats.git',
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }

        stage('Security Scans') {
            parallel {
                stage('Bandit') {
                    steps {
                        sh 'bandit -r . -f xml -o bandit-results.xml'
                    }
                    post {
                        always {
                            archiveArtifacts 'bandit-results.xml'
                        }
                    }
                }
                stage('CodeQL') {
                    steps {
                        sh 'python -m venv $VENV_DIR'
                        sh '. $VENV_DIR/bin/activate && pip install -r requirements.txt'
                        sh 'codeql database create --language=python codeql-db'
                    }
                }
            }
        }

        stage('Quality Checks') {
            steps {
                sh 'pylint **/*.py --output-format=parseable > pylint-report.txt'
                warnings(
                    canComputeNew: false,
                    canResolveRelativePaths: false,
                    defaultEncoding: '',
                    excludePattern: '',
                    healthy: '',
                    includePattern: '',
                    messagesPattern: '',
                    unHealthy: '',
                    tool: pyLint(id: 'pylint', name: 'Pylint', pattern: 'pylint-report.txt')
                )
            }
        }

        stage('Test & Coverage') {
            steps {
                sh '$PYTHON -m pytest --cov=api --cov-report=xml:coverage.xml'
            }
        }
    }
    post {
        always {
            cleanWs()
            script {
                currentBuild.description = "Build #${currentBuild.number} - ${currentBuild.result}"
            }
        }
    }
}
