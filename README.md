Tasks:
- Automatization preparing a system for  application deploy: create users,  install system depends, set up firewall; 
- Containerize all app component: database, application code, load balancing; 
- Set up CI/CD process with test web app; 

Solutions:

As we going to use docker containerization, main idea here it is up docker ecosystem on host VM and ensure it is work stable.
Also we need think about basic network security. Ensure users have enough privilege for system management, jenkins user
needs special privilege for docker service access. This scope of tasks developing with [ansible playbook](https://github.com/yougooo/ansible).


