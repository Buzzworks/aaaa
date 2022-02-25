#!/bin/bash
##################################################################################
# Redis Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports :  Ubuntu,Debian, CentOS, Redhat
###################################################################################

##Redirect the console error and output
exec > ~/redis-install.log 2>&1

##load global Environment variable
source /etc/environment

docker pull redis
docker run --rm -d --name redis redis
#docker cp redis:/etc/redis.conf /etc/redis.conf
#sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis.conf
mkdir -p /var/lib/redis/data/
docker stop redis

cat <<EOT >/etc/systemd/system/redis-docker.service
[Unit]
Description=Redis Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull redis
ExecStart=/usr/bin/docker run --rm -p 0.0.0.0:6379:6379 -v /var/lib/redis/data/:/var/lib/redis/data/ --name redis redis
ExecStop=/usr/bin/docker stop redis

[Install]
WantedBy=multi-user.target
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=6379/tcp --permanent
#firewall-cmd --reload

systemctl enable redis-docker
systemctl start redis-docker