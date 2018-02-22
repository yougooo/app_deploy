[app link](http://35.198.91.243/)

Tasks:
- Automation preparing a system for  application deploy: create users,  install system depends, set up firewall; 
- Containerize all app component: database, application code, load balancing; 
- Set up CI/CD process with test web app; 

Solutions:

As we going to use docker containerization, main idea here it is up docker ecosystem on host VM and ensure it is work stable.
Also we need think about basic network security. Ensure users have enough privilege for system management, jenkins user
needs special privilege for docker service access. This scope of tasks developing with [ansible playbook](https://github.com/yougooo/ansible). After running this roles we have environment ready to setup CI/CD workflows. 

Start from [simple Django](https://github.com/yougooo/app_deploy/tree/master/library/books_storage) MVC(MVT in Django specificity) app. App just provide searching  in database and present result to user, nothing special, but good point for start containerization, because pattern MVT(Model View Templatee) commonly come with database, static file, frontend and backend frameworks, web servers, many other feature which we can put into container. Below database schema:    
![alt text](https://github.com/yougooo/epam_training/blob/master/Python/final_project/database/database_schema.png)

Continuous integration start from automating application build, also we need think about some "quality gates", for answer to question, "Can I release today?". In Jenkins we start from new pipeline project, with Jenkins file we can define the logic of our pipeline. Jenkins support groovy very powerful(for instance we can define parallel jobs) scripting language with Java friendly syntax. Below Dockerfile, with this we put our Django app code to python image and install app depend. 

```DOCKERFILE
FROM python:3.5
ENV PYTHONUNBUFFERED 1  
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code
WORKDIR /code/library
```

With github and Jenkins plugin for github, add credential for github api access, after this we may start webhooks listening for full automation build process.
![alt text](http://makescreen.ru/i/dc4c066dd6f284e60a6bdd187181cf.png)

After any commit to master branch, jenkins start running build with Dokerfile, after successful build jenkins push new image to public registry. Below Jenkins file, from this point we have CI: 

```groovy
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
```

Continuous delivery start from continuous integration + more test automation + automation deployment artifacts, very close to continuous deployment, but here some action may done manual, like button "deploy to production". 

```groovy
   stage('Deploy image'){
         sh "docker pull yougooo/library_app:latest"
         sh "docker-compose up -d"
         sh "docker-compose scale web=3"
    }

    stage('Update nginx upstream'){
         sh "python conf_generator.py"
         sh "docker-compose restart nginx"
    }
```
![alt text](http://makescreen.ru/i/5aa899e4ce9e3c273ff34ad18ee055.png)

So app in test, production or any other environments need database and webserver. Below demonstrate model how components interact with each other. 
<p align="center"><img src =http://makescreen.ru/i/ebc3a8e4b84139b3d924977481dcfb.png /></p>

Django have simple implementation HTTP servers, but it is only for quick developers test, not for production. That's why we need one more HTTP server. Pure python web framework like Flask, Tornado, Django, etc, don't know HTTP protocol. Here help WSGI(Web Server Gateway Interface) it is specification which give standard how python web application and web servers can interact. Okay but with default configurations web server like Apache or Nginx, don't know WSGI. It is mean we need web server which know WSGI and HTTP, in my case it is gunicorn. So in app nodes run gunicorn and connected to database container, with Nginx upstream call app nodes. 

Below docker-compose file which may define how app componets look like in production, or any other environments.

```yml
version: '2'  

services:  
  
  nginx:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - web
    volumes:
      - ./static:/static
      - ./config/nginx:/etc/nginx/conf.d

  web:
    image: yougooo/library_app:latest 
    command: bash -c "gunicorn --env DJANGO_SETTINGS_MODULE=library.settings.local library.wsgi -b 0.0.0.0:8000"
    depends_on:
      - db
    volumes:
      - ./static:/static

  db:
    image: yougooo/library_db
    restart: always
    environment:
      POSTGRES_USER: alex
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: library
```
Database image build from base PostgreSQL image, with sql dump which run from default postgres ENTRYPOINT, it is mean database restore only when image start running. Maybe in production better use just process in container which connected for example to GCP sql instance. But in other cases docker database image is very fast way for deploy. 

```DOCKERFILE
FROM postgres:alpine
ADD postgres_db_dump.sql /docker-entrypoint-initdb.d
ADD restore.sh /docker-entrypoint-initdb.d
```

Share volume ./static to containers application and nginx, then define alias for static files in nginx config. Because gunicorn not very good solution for handle static files.

Quick fix for updating nginx upstream, [conf generator](https://github.com/yougooo/app_deploy/blob/master/conf_generator.py) with jinja2 templats.   

```python
def render_conf(docker_id_list):
    j2_env = Environment(loader=FileSystemLoader(CURRENT_DIR), trim_blocks=True)
    conf = j2_env.get_template('conf_template.j2').render(ids=docker_id_list)
    return conf


def main(conf):
    with open('config/nginx/django.conf', 'w') as save:
        for line in conf.split('\n'):
            save.write(line + '\n')
    return 0
```

[app link](http://35.198.91.243/)

