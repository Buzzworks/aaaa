#!/bin/bash
##################################################################################
# Nginx Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,CentOS, Redhat
###################################################################################

docker pull nginx

mkdir -p /etc/nginx/conf.d
mkdir -p /etc/ssl
cp nginx.conf /etc/nginx/
cp -r conf.d /etc/nginx/

##SSL Certificate Generation Script
source flexycrt.sh

mkdir -p /home/app/

printf "To Authenticate enter Personal Access Token to pull docker image.\n"

docker login -u vedakatta ## Enter Personal Access Token at prompt
docker pull vedakatta/flexydial-static

docker run -dit --rm --name flexy-static vedakatta/flexydial-static
docker cp flexy-static:/home/app/static/ /home/app

cp nginx-docker.service /etc/systemd/system/

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=80/tcp --permanent
#firewall-cmd --add-port=443/tcp --permanent
#firewall-cmd --add-port=7444/tcp --permanent
#firewall-cmd --add-port=3232/tcp --permanent
#firewall-cmd --reload

systemctl enable nginx-docker
systemctl start nginx-docker