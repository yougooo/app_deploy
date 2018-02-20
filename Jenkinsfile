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
         sh "docker-compose up -d"
         sh "docker-compose up -d --no-deps --build web"
    }

    stage('Update nginx upstream'){
         sh "python conf_generator.py"
         sh "docker-compose up -d"
         sh "ls config/nginx"
    }
}
