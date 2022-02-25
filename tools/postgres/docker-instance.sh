#!/bin/bash
##################################################################################
# Postgresql Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,Debian, CentOS, Redhat
###################################################################################
##Redirect the console error and output
exec > ~/db-install.log 2>&1

##load global Environment variable
source /etc/environment

docker pull postgres:14
mkdir -p /var/lib/postgresql/data/
cat <<EOT >/etc/systemd/system/postgres-docker.service
[Unit]
Description=PostgreSQL DB Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull postgres:14
ExecStart=/usr/bin/docker run --rm -p 0.0.0.0:5432:5432 --env-file /etc/default/flexydial-db -v /opt/docker-postgres.sql:/docker-entrypoint-initdb.d/docker_postgres_init.sql -v /var/lib/postgresql/data:/var/lib/postgresql/data  --name postgres-db postgres
ExecStop=/usr/bin/docker stop postgres-db

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT >/opt/docker-postgres.sql
CREATE DATABASE crm
    WITH
    OWNER = flexydial
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
EOT

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