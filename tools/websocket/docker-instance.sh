#!/bin/bash
##################################################################################
# Flexydial WebSocket Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,CentOS, Redhat
###################################################################################

printf "To Authenticate enter Personal Access Token to pull docker image.\n"

docker login -u vedakatta ## Enter Personal Access Token at prompt
docker pull vedakatta/flexydial-websocket

cp flexydial-websocket-docker.service /etc/systemd/system/

cat <<EOT >> /etc/default/flexydial-websocket
HOST_URL=web
REDIS_URL=redis
REDIS_PORT=6379
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=3232/tcp --permanent
#firewall-cmd --reload

systemctl enable flexydial-websocket-docker
systemctl start flexydial-websocket-docker
