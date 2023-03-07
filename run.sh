#!/bin/bash

# Ejecutar el aprovisionamiento de Ansible en un servidor remoto

ansible-playbook -i inventory.ini provision.yml
