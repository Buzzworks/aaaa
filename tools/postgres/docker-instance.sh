#!/bin/bash
##################################################################################
# Postgresql Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,CentOS, Redhat
###################################################################################

docker pull postgres:14

cp postgres-docker.service /etc/systemd/system/
cp docker-postgres.sql /opt/

cat <<EOT > /etc/default/flexydial-db
DATABASE_HOST=127.0.0.1
POSTGRES_USER=flexydial
POSTGRES_PASSWORD=flexydial
POSTGRES_DB=flexydial
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=5432/tcp --permanent
#firewall-cmd --reload

systemctl enable postgres-docker
systemctl start postgres-docker
docker exec -it postgres-db psql -d flexydial -Uflexydial -c 'create extension hstore;'
docker exec -it postgres-db psql -d crm -Uflexydial -c 'create extension hstore;'