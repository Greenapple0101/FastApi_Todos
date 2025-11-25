pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'   // DockerHub 자격증명 ID
        IMAGE_NAME            = 'yorange50/fastapi-app' // 빌드·푸시할 이미지 이름
        REMOTE_USER           = 'ubuntu'                 // 배포 대상 서버 유저
        REMOTE_HOST           = '3.34.155.126'              // 배포 대상 서버 호스트
        REMOTE_PATH           = '/home/ubuntu'           // 배포용 디렉토리
        COMPOSE_FILE          = 'docker-compose.yml'
        SONAR_TOKEN           = credentials('sonar-token')
        SONAR_HOST_URL        = 'http://localhost:9000'
        JMETER_IMAGE_NAME     = 'my-arm-jmeter'
    }

    stages {
        stage('Checkout') {
            steps {
                git url:  'https://github.com/Greenapple0101/FASTAPI-APP.git', branch: 'main'
            }
        }

        stage('Setup Environment & Install Dependencies') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-venv python3-pip git
                    python3 -m venv venv
                    . venv/bin/activate                   
                    pip install -r fastapi-app/requirements.txt             
                '''
            }
        }

        stage('Test & Coverage') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="$PYTHONPATH:$(pwd)/fastapi-app"
                    mkdir -p pytest_report
                    pytest fastapi-app/tests \
                        --html=pytest_report/report.html \
                        --self-contained-html \
                        --cov=fastapi-app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html:htmlcov
                    cp coverage.xml fastapi-app/coverage.xml
                '''
            }
            post {
                always {
                    publishHTML(target: [
                        reportName         : 'Pytest HTML Report', 
                        reportDir          : 'pytest_report',
                        reportFiles        : 'report.html',
                        keepAll            : true,
                        alwaysLinkToLastBuild: true,
                        allowMissing       : false
                    ])
                    publishHTML(target: [
                        reportName         : 'Coverage Report', 
                        reportDir          : 'htmlcov',
                        reportFiles        : 'index.html',
                        keepAll            : true,
                        alwaysLinkToLastBuild: true,
                        allowMissing       : false
                    ])
                }
            }
        }

        stage('Build JMeter Image') {
            steps {
                dir('jmeter') {
                    script {
                        docker.build("${JMETER_IMAGE_NAME}:latest", ".")
                    }
                }
            }
        }

        stage('Run JMeter Load Test') {
            steps {
                dir('jmeter') {
                    script {
                        docker.image("${JMETER_IMAGE_NAME}:latest").inside('--network host --user root:root') {
                            sh '''
                                rm -rf report jmeter.log results.jtl
                                mkdir -p report
                                jmeter -n \
                                       -t fastapi_test_plan.jmx \
                                       -JBASE_URL=http://3.34.155.126:5001 \
                                       -l results.jtl \
                                       -Jjmeter.save.saveservice.output_format=csv \
                                       -e -o report
                            '''
                        }
                    }
                }
            }
            post {
                always {
                    publishHTML(target: [
                        reportName           : 'JMeter HTML Report',
                        reportDir            : 'jmeter/report',
                        reportFiles          : 'index.html',
                        keepAll              : true,
                        alwaysLinkToLastBuild: true,
                        allowMissing         : false
                    ])
                }
            }
        }

        stage('Build') {
            steps {
                dir('fastapi-app') {
                    script {
                        docker.build("${IMAGE_NAME}:latest", ".")
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image("${IMAGE_NAME}:latest").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['ubuntu']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@3.34.155.126 '
                            docker pull yorange50/fastapi-app:latest &&
                            docker rm -f FastApi-app || true &&
                            docker run -d --name FastApi-app -p 5001:5001 yorange50/fastapi-app:latest
                        '
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
