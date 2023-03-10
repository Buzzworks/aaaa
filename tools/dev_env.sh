#!/bin/bash

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
REDIS_PORT=6379
DEBUG=TRUE
DEVELOPMENT=TRUE
RABBITMQ_HOST=${RABBITMQ_HOST}
EOT

cat <<EOT > /etc/default/flexydial-websocket
HOST_URL=${APP_HOST}
REDIS_URL=${REDIS_HOST}
REDIS_PORT=6379
EOT

cat <<EOT > /etc/default/flexydial-db
DATABASE_HOST=127.0.0.1
POSTGRES_USER=flexydial
POSTGRES_PASSWORD=flexydial
POSTGRES_DB=flexydial
EOT
