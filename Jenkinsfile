pipeline {
    agent {
        label 'windows-local'
    }
    options {
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }
    environment {
        VENV_PATH = 'F:\\CodeBase\\Steam-Stats\\venv'
        CODECOV_TOKEN = credentials('codecov-token')
    }
    stages {
        stage('Environment Setup') {
            steps {
                bat """
                    echo Using existing virtual environment at %VENV_PATH%
                    call "%VENV_PATH%\\Scripts\\activate"
                    python -V
                    pipdeptree
                """
            }
        }

        stage('Security Scan') {
            steps {
                bat """
                    call "%VENV_PATH%\\Scripts\\activate"
                    echo Running Bandit security scan
                    bandit -r . -f json -o bandit-report.json
                """
                archiveArtifacts 'bandit-report.json'
            }
        }

        stage('Quality Checks') {
            steps {
                bat """
                    call "%VENV_PATH%\\Scripts\\activate"
                    echo Running Pylint analysis
                    pylint api tests --output-format=parseable > pylint-report.txt
                """
                warnings(
                    tool: pyLint(id: 'pylint', name: 'Pylint', pattern: 'pylint-report.txt')
                )
            }
        }

        stage('Test & Coverage') {
            steps {
                bat """
                    call "%VENV_PATH%\\Scripts\\activate"
                    echo Running tests with coverage
                    pytest --cov=api --cov-report=xml:coverage.xml --junitxml=test-results.xml

                    echo Uploading to Codecov
                    curl -Os https://uploader.codecov.io/latest/windows/codecov.exe
                    codecov.exe -f coverage.xml -t %CODECOV_TOKEN% -B %GIT_BRANCH% -C %GIT_COMMIT%
                """
                junit 'test-results.xml'
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
