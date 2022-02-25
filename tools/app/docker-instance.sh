#!/bin/bash
##################################################################################
# Flexydial Application Installation script
# Version: 1.0
# Author: Ganapathi Chidambaram < ganapathi.chidambaram@flexydial.com >
# Supports : Ubuntu,Debian, CentOS, Redhat
###################################################################################
exec > ~/app-install.log 2>&1

source /etc/environment

docker login -u vedakatta -p ${DOCKER_TOKEN}

docker pull vedakatta/flexydial-app

mkdir -p /var/run/app

cat <<EOT > /etc/systemd/system/flexydial-app-docker.service
[Unit]
Description=FlexyDial App V4 Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull vedakatta/flexydial-app
ExecStart=/usr/bin/docker run --rm -v /var/run/app:/var/run/app -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-app vedakatta/flexydial-app uwsgi --disable-logging --ini uwsgi-unix.ini
ExecStop=/usr/bin/docker stop flexydial-app

[Install]
WantedBy=multi-user.target
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
ExecStart=/usr/bin/docker run --rm -v /var/lib/flexydial/media:/var/lib/flexydial/media --env-file /etc/default/flexydial-app --name flexydial-manager vedakatta/flexydial-app python manage.py manager
ExecStop=/usr/bin/docker stop flexydial-manager

[Install]
WantedBy=multi-user.target
EOT

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
EOT

# Redhat-Based command for firewall entry when container running with host networking
#firewall-cmd --add-port=5432/tcp --permanent
#firewall-cmd --reload

mkdir -p /var/lib/flexydial/media

systemctl enable flexydial-app-docker
systemctl start flexydial-app-docker

####Nginx start

docker pull nginx

mkdir -p /etc/nginx/conf.d
mkdir -p /etc/ssl

cat <<'EOT' > /etc/nginx/nginx.conf
user  root;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
               '$status $body_bytes_sent "$http_referer" '
               '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    # Gzip Compression
    gzip on;
    # gzip_min_length 1000;
    gzip_types text/plain application/xml;
    gzip_proxied expired no-cache no-store private auth;
    gzip_vary on;

     include /etc/nginx/conf.d/*.conf;
    #include /etc/nginx/sites-available/*;
}
EOT

cat <<'EOT' > /etc/nginx/conf.d/default.conf
# the upstream component nginx needs to connect to
upstream uwsgi {
    server unix:/var/run/app/app.sock; # for a file socket
    #server 127.0.0.1:8001;
}
upstream socket_ws {
 ip_hash;
 server  ${SOCKET_HOST}:3233; # Mention WebSocket Server IP address/domain name
}
upstream telephony_ws {
 ip_hash;
 server  ${TELEPHONY_HOST}:7443; # Mention Telephony Server IP address/domain name
}
# configuration of the server
server {
    listen    80;
    return 301 https://$host$request_uri;
}
# configuration of the server
server {
  listen 443 default_server ssl;
  ssl_certificate /etc/ssl/flexydial.crt;
  ssl_certificate_key /etc/ssl/flexydial.key;
  ssl_certificate /etc/ssl/wss.pem;
  ssl_certificate_key /etc/ssl/wss.pem;
  charset     utf-8;
  #client_max_body_size 75M;   # adjust to taste
  client_body_timeout 300s;
  uwsgi_read_timeout 300s;
  location /static
  {
    alias /home/app/static; # your Django project's static files - amend as required
  }
  location /nginx/status {
      stub_status on;
      # access_log /usr/local/nginx/logs/status.log;
      access_log off;
      auth_basic "NginxStatus";
  }
  location / {
      include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
      uwsgi_pass  uwsgi;
      proxy_set_header Host            $host;
      proxy_set_header X-Forwarded-For $remote_addr;
  }
  location /socket.io {
      proxy_pass  https://socket_ws;
      proxy_set_header Host            $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_read_timeout 86400;
  }
  location /wss {
    proxy_pass https://telephony_wss;
    proxy_set_header Host            $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
  }
}
server {
  listen 7444 default_server ssl;
  ssl_certificate /etc/ssl/flexydial.crt;
  ssl_certificate_key /etc/ssl/flexydial.key;

  server_name _;
  location / {
    proxy_pass https://telephony_wss;
    proxy_set_header Host            $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
  }
}
EOT

## Added this line due to terraform userdata and local installation
cp flexycrt.sh /opt/

##SSL Certificate Generation Script
pushd /opt/
chmod +rx flexycrt.sh
/bin/bash flexycrt.sh
popd

mkdir -p /home/app/

docker pull vedakatta/flexydial-static

docker run -dit --rm --name flexy-static vedakatta/flexydial-static
docker cp flexy-static:/home/app/static/ /home/app
docker stop flexy-static

cat <<EOT > /etc/systemd/system/nginx-docker.service
[Unit]
Description=Nginx Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=1
#ExecStartPre=/usr/bin/docker pull nginx
ExecStart=/usr/bin/docker run --rm -p 0.0.0.0:443:443 -p 0.0.0.0:80:80 -p 0.0.0.0:3232:3232 -v /var/run/app:/var/run/app -v /home/app/static:/home/app/static -v /etc/nginx/nginx.conf:/etc/nginx/nginx.conf -v /etc/nginx/conf.d/default.conf:/etc/nginx/conf.d/default.conf -v /etc/ssl:/etc/ssl --name nginx nginx nginx -g 'daemon off;'
ExecStop=/usr/bin/docker stop nginx

[Install]
WantedBy=multi-user.target
EOT
systemctl enable nginx-docker
systemctl start nginx-docker

####Nginx End

docker exec  flexydial-app python manage.py makemigrations
docker exec  flexydial-app python manage.py migrate callcenter
docker exec  flexydial-app python manage.py migrate crm --database=crm
docker exec  flexydial-app python manage.py migrate django_apscheduler
docker exec  flexydial-app python manage.py migrate auth
docker exec  flexydial-app python manage.py migrate sessions
docker exec  flexydial-app python manage.py migrate crm --fake
docker exec  flexydial-app python manage.py dummy_fixture

cp flexydial-autodial-docker.service /etc/systemd/system/
cp flexydial-cdrd-docker.service /etc/systemd/system/

systemctl enable flexydial-autodial-docker
systemctl start flexydial-autodial-docker

systemctl enable flexydial-cdrd-docker
systemctl start flexydial-cdrd-docker