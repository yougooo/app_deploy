#!/usr/bin/env groovy

node {
    def app
    
    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("django/images:${env.BUILD_NUMBER}")
    }

    stage('Push image') {
            docker.withRegistry('https://hub.docker.com', 'docker-credentials') {
            app.push("latest")
        }
    }
}
