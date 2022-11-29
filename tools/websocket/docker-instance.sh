#!/bin/bash
##################################################################################
# Flexydial WebSocket Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,Debian,CentOS, Redhat
###################################################################################

##Redirect the console error and output
exec > ~/websocket-install.log 2>&1

##load global Environment variable
source /etc/environment

if [ "${ENV}" != "DEV" ]; then
    docker login -u vedakatta -p ${DOCKER_TOKEN}
    docker pull vedakatta/flexydial-websocket

echo "prod"
cat <<EOT > /etc/systemd/system/flexydial-websocket-docker.service
[Unit]
Description=Flexydial Websocket Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-websocket
ExecStart=/usr/bin/docker run --rm -p 0.0.0.0:3233:3233 -p 0.0.0.0:8084-8087:8084-8087 --env-file /etc/default/flexydial-websocket -v /var/lib/flexydial/media:/var/lib/flexydial/media --name flexydial-websocket websocket 
ExecStop=/usr/bin/docker stop flexydial-websocket

[Install]
WantedBy=multi-user.target
EOT
else
echo "dev"
sh ../../fs-dialplan/dev_setup.sh 
cat <<EOT > /etc/systemd/system/flexydial-websocket-docker.service
[Unit]
Description=Flexydial Websocket Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-websocket
ExecStart=/usr/bin/docker run --rm -p 0.0.0.0:3233:3233 -p 0.0.0.0:8084-8087:8084-8087 --env-file /etc/default/flexydial-websocket -v ${APP_PATH}/fs-dialplan:/home/app/fs-dialplan -v /var/lib/flexydial/media:/var/lib/flexydial/media --name flexydial-websocket flexydial-websocket 
ExecStop=/usr/bin/docker stop flexydial-websocket

[Install]
WantedBy=multi-user.target
EOT
fi

cat <<EOT > /etc/default/flexydial-websocket
HOST_URL=${APP_HOST}
REDIS_URL=${REDIS_HOST}
REDIS_PORT=6379
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=3232/tcp --permanent
#firewall-cmd --reload

systemctl enable flexydial-websocket-docker
systemctl start flexydial-websocket-docker
