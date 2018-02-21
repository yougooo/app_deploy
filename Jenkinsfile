#!/usr/bin/env groovy

node {
    def app
    
    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("yougooo/library_app:${env.BUILD_NUMBER}")
    }

    stage('Push image') {
            docker.withRegistry('https://registry.hub.docker.com', 'docker-credentials') {
            app.push("latest")
        }
    }

    stage('Deploy image'){
         sh "docker-compose down"
         sh "docker-compose up -d"
         sh "docker-compose scale web=5"
    }

    stage('Update nginx upstream'){
         sh "python conf_generator.py"
         sh "docker-compose restart nginx"
    }
}
