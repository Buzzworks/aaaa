#!/bin/bash
##################################################################################
# Flexydial dev WebSocket Docker Installation script
# Version: 1.0
# Author: ManojKumar < manoj.gundeti@flexydial.com >
# Supports : Ubuntu,Debian,CentOS, Redhat
###################################################################################

##Redirect the console error and output
# exec > ~/dev-websocket-install.log 2>&1

##load global Environment variable
source /etc/environment

docker build -t flexydial-websocket . 
# docker login -u vedakatta -p ${DOCKER_TOKEN}
# docker pull vedakatta/flexydial-websocket
cat <<EOT > /etc/default/flexydial-websocket
HOST_URL=${APP_HOST}
REDIS_URL=${REDIS_HOST}
REDIS_PORT=6379
EOT
docker run --rm -d -p 0.0.0.0:3233:3233 -p 0.0.0.0:8084-8087:8084-8087 --env-file /etc/default/flexydial-websocket -v /var/lib/flexydial/media:/var/lib/flexydial/media --name flexydial-websocket flexydial-websocket

docker cp flexydial-websocket:/home/app/fs-dialplan ${APP_PATH}/

docker stop flexydial-websocket
