#!/bin/bash
##################################################################################
# Docker Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu, CentOS, Redhat
###################################################################################
#Variables
OS_NAME=$(cat /etc/os-release | grep "NAME=" | cut -c 6- | sed 1q | sed -e 's/^"//' -e 's/"$//')
OS_VERSION=$(cat /etc/os-release | grep  "VERSION_ID=" |  cut -c 12- | sed -e 's/^"//' -e 's/"$//')

function ubuntu(){
#UBUNTU_VERSION=$1
#UBUNTU_VERSION_ROUND=$(echo "$1" | cut -b 1,2 )
UBUNTU_CODENAME=$(cat /etc/os-release | grep "VERSION_CODENAME" | cut -c 18- )

echo "Installing Docker for ubuntu CODENAME: $UBUNTU_CODENAME"
apt update -y && apt install apt-transport-https ca-certificates curl software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $UBUNTU_CODENAME stable" && apt update -y && apt-cache policy docker-ce && apt install docker-ce -y && echo "Docker Installation Done for Ubuntu"

echo "Installing Docker compose now"
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
echo "Done installing Docker compose"
}

function centos(){
echo "Installing Docker for CentOS"
cat <<EOT >> /etc/yum.repos.d/docker-ce.repo
[docker-ce-stable]
name=Docker CE Stable - \$basearch
baseurl=https://download.docker.com/linux/centos/\$releasever/\$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
EOT
yum update -y && yum install -y docker-ce docker-ce-cli containerd.io && systemctl start docker && echo "Docker Installation Done"
echo "Installing Docker compose now"
sudo curl -L https://github.com/docker/compose/releases/download/2.0.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
echo "Done installing Docker compose"
}

#Print OS Details
echo "OS: $OS_NAME"
echo "OS VERSION: $OS_VERSION"

#Conditions as per OS
if [ "$OS_NAME" == "ubuntu" ] || [ "$OS_NAME" == "Ubuntu" ] || [ "$OS_NAME" == "UBUNTU" ];
then
        ubuntu
fi
if [ "$OS_NAME" == "centos" ] || [ "$OS_NAME" == "CentOs" ] || [ "$OS_NAME" == "CentOs" ] || [ "$OS_NAME" == "CENTOS" ];
then
        centos
fi

if [ "$OS_NAME" == "redhat" ] || [ "$OS_NAME" == "RedHat" ] || [ "$OS_NAME" == "Redhat" ] || [ "$OS_NAME" == "Red Hat Enterprise Linux" ];
then
        centos
fi
