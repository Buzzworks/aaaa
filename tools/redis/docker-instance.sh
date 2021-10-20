#!/bin/bash
##################################################################################
# Redis Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports :  Ubuntu,CentOS, Redhat
###################################################################################

docker pull redis
docker run --rm -d --name redis redis
docker cp redis:/etc/redis.conf /etc/redis.conf
sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis.conf
mkdir -p /var/lib/redis/data/
docker stop redis
docker rm redis
cp redis-docker.service /etc/systemd/system/

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=6379/tcp --permanent
#firewall-cmd --reload

systemctl enable redis-docker
systemctl start redis-docker