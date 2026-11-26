// Local Jenkins CI for synthetic UDS diagnostic analysis.
// Reuses the existing Docker-based Python agent (label: aeb-python).
// This pipeline does NOT call a hosted LLM or run real ECU diagnostics.
pipeline {
    agent {
        label 'aeb-python'
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(
            numToKeepStr: '20',
            artifactNumToKeepStr: '20'
        ))
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cleaning the UDS job workspace and checking out GitHub'
                deleteDir()
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Preparing an isolated Python environment'
                sh '''
                    set -eu
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Checking published synthetic sources for common secret patterns'
                sh '''
                    set -eu
                    python3 scripts/check_public_safety.py \
                        original/ agents/automotive-uds.md \
                        examples/ uds_demo.py tests/
                '''
            }
        }

        stage('UDS Unit Tests') {
            steps {
                echo 'Testing both the original and the demonstration UDS analyzers'
                sh '''
                    set -eu
                    PYTHONPATH=original:. .venv/bin/python -m pytest -v \
                        tests/test_uds_demo.py original/test_uds_analyzer.py \
                        --junitxml=test-results.xml \
                        --cov=uds_demo --cov=uds_analyzer --cov-branch \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml
                '''
            }

            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: false
                    archiveArtifacts artifacts: 'coverage.xml',
                        allowEmptyArchive: true, fingerprint: true
                }
            }
        }

        stage('Synthetic Reports') {
            steps {
                echo 'Generating sample UDS analysis reports (no company data)'
                sh '''
                    set -eu
                    mkdir -p reports
                    .venv/bin/python uds_demo.py \
                        examples/synthetic_uds_responses.csv \
                        > reports/synthetic_uds_summary.txt
                    .venv/bin/python original/uds_analyzer.py \
                        > reports/original_uds_summary.txt
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.txt',
                allowEmptyArchive: true, fingerprint: true
        }
        success {
            echo 'UDS CI passed. Inspect the JUnit tests, coverage and synthetic reports.'
        }
        failure {
            echo 'UDS CI failed. Check the first failing stage and console output.'
        }
    }
}
