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
         sh "docker pull yougooo/library_app:latest"
         sh "docker-compose up -d"
         sh "docker-compose scale web=3"
    }

    stage('Update nginx upstream'){
         sh "python conf_generator.py"
         sh "docker-compose restart nginx"
         sh "cat conf.log"
    }
}
