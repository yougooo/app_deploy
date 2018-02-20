#!/usr/bin/env/python

from jinja2 import Environment, FileSystemLoader
import os
import re
import subprocess

pattern = re.compile("(.{12})        yougooo/library_app")
docker_image_data = subprocess.Popen("docker ps", shell=True, stdout=subprocess.PIPE)
out = docker_image_data.stdout.read()
app_id_list = pattern.findall(out)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def render_conf(docker_id_list):
    j2_env = Environment(loader=FileSystemLoader(CURRENT_DIR), trim_blocks=True)
    conf = j2_env.get_template('conf_template.j2').render(ids=docker_id_list)
    print(conf)
    return conf


def main(conf):
    with open('config/nginx/django.conf', 'w') as save:
        for line in conf.split('\n'):
            save.write(line + '\n')
    return 0


if __name__ == '__main__':
    to_save = render_conf(app_id_list)
    main(to_save)
