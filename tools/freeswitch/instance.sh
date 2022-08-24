#!/bin/bash
##################################################################################
# Freeswitch Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu-20.04,Debian-11, CentOS, Redhat
###################################################################################
##Redirect the console error and output

exec > ~/freeswitch-install.log 2>&1

##load global Environment variable
source /etc/environment


OS_NAME=$(cat /etc/os-release | grep "^NAME=" | cut -c 6- | sed 1q | sed -e 's/^"//' -e 's/"$//' | awk '{print $1}')
OS_VERSION=$(cat /etc/os-release | grep  "VERSION_ID=" |  cut -c 12- | sed -e 's/^"//' -e 's/"$//')

function debian(){
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/Debian_11/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/Debian_11/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt -y update
sudo apt -y install freeswitch freeswitch-meta-flexydial freeswitch-mod-lua  freeswitch-mod-shout  freeswitch-mod-xml-curl freeswitch-mod-xml-rpc
cp /usr/share/freeswitch/conf/flexydial /etc/freeswitch/ -r
}
function ubuntu(){
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt -y update
sudo apt -y install freeswitch freeswitch-meta-flexydial freeswitch-mod-lua  freeswitch-mod-shout  freeswitch-mod-xml-curl freeswitch-mod-xml-rpc
cp /usr/share/freeswitch/conf/flexydial /etc/freeswitch/ -r
}

function redhat(){
cat <<EOT > /etc/yum.repos.d/flexydial.repo
[Flexydial_Repo]
name=Flexydial Repo - RHEL-\$releasever-\$basearch
baseurl=http://flexy-repo.s3-website-us-east-1.amazonaws.com/rhel/\$releasever/\$basearch
enabled=1
gpgkey=http://flexy-repo.s3-website-us-east-1.amazonaws.com/RPM-GPG-KEY-ganapathi
gpgcheck=1
EOT
sudo dnf install freeswitch-config-flexydial -y
sudo systemctl enable freeswitch
sudo systemctl start freeswitch
}


#Conditions as per OS
if [ "$OS_NAME" == "ubuntu" ] || [ "$OS_NAME" == "Ubuntu" ] || [ "$OS_NAME" == "UBUNTU" ];
then
        ubuntu
fi
if [ "$OS_NAME" == "debian" ] || [ "$OS_NAME" == "Debian" ] || [ "$OS_NAME" == "DEBIAN" ];
then
        debian
fi
if [ "$OS_NAME" == "centos" ] || [ "$OS_NAME" == "CentOs" ] || [ "$OS_NAME" == "CentOs" ] || [ "$OS_NAME" == "CENTOS" ];
then
        redhat
fi

if [ "$OS_NAME" == "redhat" ] || [ "$OS_NAME" == "RedHat" ] || [ "$OS_NAME" == "Redhat" ] || [ "$OS_NAME" == "Red Hat Enterprise Linux" ];
then
        redhat
fi



EOT
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

cat <<EOT > /etc/systemd/system/flexydial-cdrd-docker.service
[Unit]
Description=FlexyDial CDR Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm --env-file /etc/default/flexydial-app --name flexydial-cdr vedakatta/flexydial-app python manage.py cdrd
ExecStop=/usr/bin/docker stop flexydial-cdr

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT > /etc/systemd/system/flexydial-autodial-docker.service
[Unit]
Description=FlexyDial AutoDial Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-autodial vedakatta/flexydial-app python manage.py autodial
ExecStop=/usr/bin/docker stop flexydial-autodial

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT > /etc/systemd/system/flexydial-audio-fs-docker.service
[Unit]
Description=FlexyDial Audio File transfer Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-audio-fs vedakatta/flexydial-app python manage.py audio_callserver
ExecStop=/usr/bin/docker stop flexydial-audio-fs

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

cat <<EOT > /etc/systemd/system/flexydial-cdrd-docker.service
[Unit]
Description=FlexyDial CDR Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm --env-file /etc/default/flexydial-app -v ${APP_PATH}:/home/app --name flexydial-cdr flexydial-app python manage.py cdrd
ExecStop=/usr/bin/docker stop flexydial-cdr

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT > /etc/systemd/system/flexydial-autodial-docker.service
[Unit]
Description=FlexyDial AutoDial Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media -v ${APP_PATH}:/home/app --env-file /etc/default/flexydial-app --name flexydial-autodial flexydial-app python manage.py autodial
ExecStop=/usr/bin/docker stop flexydial-autodial

[Install]
WantedBy=multi-user.target
EOT


cat <<EOT > /etc/systemd/system/flexydial-audio-fs-docker.service
[Unit]
Description=FlexyDial Audio File transfer Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media -v ${APP_PATH}:/home/app --env-file /etc/default/flexydial-app --name flexydial-audio-fs flexydial-app python manage.py audio_callserver
ExecStop=/usr/bin/docker stop flexydial-audio-fs

[Install]
WantedBy=multi-user.target
EOT
fi