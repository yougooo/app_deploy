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
            docker.withRegistry('https://hub.docker.com', 'docker-credentials') {
            app.push("latest")
        }
    }
}
