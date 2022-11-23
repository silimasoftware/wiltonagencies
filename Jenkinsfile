pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker compose -f production.yml down'
                sh 'docker volume rm wiltonagenciescom_website_data'
                sh 'docker compose -f production.yml build --no-cache'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose -f production.yml up -d --force-recreate'
            }
        }
    }
}
