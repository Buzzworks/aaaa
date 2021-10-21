#!/bin/bash
##################################################################################
# Flexydial Application Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,CentOS, Redhat
###################################################################################

printf "To Authenticate enter Personal Access Token to pull docker image.\n"
docker login -u vedakatta ## Enter Personal Access Token at prompt
docker pull vedakatta/flexydial-app

cp flexydial-app-docker.service /etc/systemd/system/

cat <<EOT >> /etc/default/flexydial-app
PYTHONUNBUFFERED=1
FREESWITCH_HOST=telephony
WEB_SOCKET_HOST=web:3232
FLEXYDIAL_DB_NAME=flexydial
FLEXYDIAL_DB_USER=flexydial
FLEXYDIAL_DB_PASS=flexydial
FLEXYDIAL_DB_HOST=db
FLEXYDIAL_DB_PORT=5432
CRM_DB_NAME=crm
CRM_DB_USER=flexydial
CRM_DB_PASS=flexydial
CRM_DB_HOST=db
CRM_DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=5432/tcp --permanent
#firewall-cmd --reload

systemctl enable flexydial-app-docker
systemctl start flexydial-app-docker

docker exec -it flexydial-app python manage.py migrate callcenter
docker exec -it flexydial-app python manage.py migrate crm --database=crm
docker exec -it flexydial-app python manage.py migrate django_apscheduler
docker exec -it flexydial-app python manage.py migrate auth
docker exec -it flexydial-app python manage.py migrate sessions
docker exec -it flexydial-app python manage.py migrate crm --fake
docker exec -it flexydial-app python manage.py dummy_fixture

cp flexydial-autodial-docker.service /etc/systemd/system/
cp flexydial-cdrd-docker.service /etc/systemd/system/

systemctl enable flexydial-autodial-docker
systemctl start flexydial-autodial-docker

systemctl enable flexydial-cdrd-docker
systemctl start flexydial-cdrd-docker