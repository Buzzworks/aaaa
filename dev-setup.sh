#!/bin/bash
##################################################################################
# Flexydial dev App Docker Installation script
# Version: 1.0
# Author: ManojKumar < manoj.gundeti@flexydial.com >
# Supports : Ubuntu,Debian,CentOS, Redhat
###################################################################################

##Redirect the console error and output
# exec > ~/dev-app-install.log 2>&1

##load global Environment variable
source /etc/environment

mkdir -p /var/run/app

docker build -t flexydial-app -f Dockerfile.dev .
cat <<EOT > /etc/default/flexydial-app
FREESWITCH_HOST=${TELEPHONY_HOST}
FLEXYDIAL_DB_NAME=flexydial
FLEXYDIAL_DB_USER=flexydial
FLEXYDIAL_DB_PASS=flexydial
FLEXYDIAL_DB_HOST=${DB_HOST}
FLEXYDIAL_DB_PORT=5432
CRM_DB_NAME=crm
CRM_DB_USER=flexydial
CRM_DB_PASS=flexydial
CRM_DB_HOST=${DB_HOST}
REDIS_HOST=${REDIS_HOST}
EOT
docker run -d --rm -v /var/run/app:/var/run/app -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-app flexydial-app uwsgi --disable-logging --ini uwsgi-unix.ini

docker cp flexydial-app:/home/app ${APP_PATH}/../

docker stop flexydial-app


