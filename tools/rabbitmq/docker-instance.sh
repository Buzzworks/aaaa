#!/bin/bash

cat <<EOT >/etc/systemd/system/rabbitmq-docker.service
[Unit]
Description=Redis Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull redis
ExecStart=/usr/bin/docker run --rm -it -p 15672:15672 -p 5672:5672 -name rabbitmq-server rabbitmq:3-management
ExecStop=/usr/bin/docker stop rabbitmq-server

[Install]
WantedBy=multi-user.target
EOT

systemctl enable rabbitmq-docker
systemctl start rabbitmq-docker


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

cat <<EOT > /etc/systemd/system/rabbitmq-worker-docker.service
[Unit]
Description=FlexyDial RabbitMQ Worker Docker Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm --env-file /etc/default/flexydial-app -v ${APP_PATH}:/home/app --name rabbitmq-worker flexydial-app python manage.py progressive_worker
ExecStop=/usr/bin/docker stop rabbitmq-worker

[Install]
WantedBy=multi-user.target
EOT


systemctl enable rabbitmq-worker-docker
systemctl start rabbitmq-worker-docker