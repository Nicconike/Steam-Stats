pipeline {
    agent {
        label 'windows-local'
    }
    options {
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }
    environment {
        VENV_DIR = 'F:\\CodeBase\\Steam-Stats\\venv'
    }
    stages {
        stage('Security Scans') {
            parallel {
                stage('Bandit') {
                    steps {
                        bat 'python -m bandit -r . -f xml -o bandit-results.xml'
                    }
                    post {
                        always {
                            archiveArtifacts 'bandit-results.xml'
                        }
                    }
                }
                stage('CodeQL') {
                    steps {
                        bat 'python -m venv %VENV_DIR%'
                        bat 'call %VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt'
                        bat 'codeql database create --language=python codeql-db'
                    }
                }
            }
        }

        stage('Quality Checks') {
            steps {
                bat 'python -m pylint **/*.py --output-format=parseable > pylint-report.txt'
                warnings(
                    canComputeNew: false,
                    canResolveRelativePaths: false,
                    tool: pyLint(id: 'pylint', name: 'Pylint', pattern: 'pylint-report.txt')
                )
            }
        }

        stage('Test & Coverage') {
            steps {
                bat 'python -m pytest --cov=api --cov-report=xml:coverage.xml'
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
