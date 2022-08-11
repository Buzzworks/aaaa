
if [ "${ENV}" != "DEV" ]; then
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
EOT
docker login -u vedakatta -p ${DOCKER_TOKEN}

docker pull vedakatta/flexydial-app



cat <<EOT > /etc/systemd/system/flexydial-manager-docker.service
[Unit]
Description=FlexyDial Manager Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-manager vedakatta/flexydial-app python manage.py manager
ExecStop=/usr/bin/docker stop flexydial-manager

[Install]
WantedBy=multi-user.target
EOT



else

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
EOT

cat <<EOT > /etc/systemd/system/flexydial-manager-docker.service
[Unit]
Description=FlexyDial Manager Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media -v ${APP_PATH}:/home/app --env-file /etc/default/flexydial-app --name flexydial-manager flexydial-app python manage.py manager
ExecStop=/usr/bin/docker stop flexydial-manager

[Install]
WantedBy=multi-user.target
EOT
fi

systemctl enable flexydial-manager-docker
systemctl start flexydial-manager-docker