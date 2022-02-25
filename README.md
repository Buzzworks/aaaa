# Flexydial 6.0

[![Docker Image CI](https://github.com/Buzzworks/flexydial/actions/workflows/build-images.yaml/badge.svg)](https://github.com/Buzzworks/flexydial/actions/workflows/build-images.yaml)

## Requirements:

- Any Recent Operating System ( Redhat / CentOS / Ubuntu ).
- Python3.8
- Docker CE Stable


## Installation Steps/Hints:
- Go to tools folder and find the category based folder for the installation. Almost every instance required *docker-install.sh* before running those script.
- On Each instance export all these variables in-case if each instance running on different machine. Don't forgot to export environment variables even for standalone instance also.
- To make sure source command working before running script, so that it would load environment variable while installation.

```
echo APP_HOST=enter_ip_of_app >> /etc/environment
echo REDIS_HOST=enter_ip_of_app >> /etc/environment
echo DB_HOST=enter_ip_of_app >> /etc/environment
echo SOCKET_HOST=enter_ip_of_app >> /etc/environment
echo TELEPHONY_HOST=enter_ip_of_app >> /etc/environment
```

- Don't store token into environment. export into current session for ImagePull from Docker

```
export DOCKER_TOKEN=enter_docker_authentication
```
- *flexydial-manager-docker* service which is part of *app* should run only one instance and able to run on any standalone machine as well without any other dependencies.

- Freeswitch installation also through repository which is currently supported for ubuntu 20.04, Debian 11, Redhat 8.5. Also freeswitch instance required cdrd and autodial on the same instance as of now.

## Application Components


Each of these components mentioned below are able to run it same or different server.

- flexydial-app
- flexydial-autodial
- flexydial-cdrd
- flexydial-websocket
- flexydial-manager
- nginx
- redis
- PostgreSQL
- freeswitch

Note: Except freeswitch everything based on docker image for quicker installation and other management activity.
Unable to use docker for freeswitch due to heavy RTP port range through docker proxy, so advised to use
 ``--network host`` to avoid freeswitch hosting container crash while start.
So considering this all fact, standalone installation is more preferred for freeswitch mostly.

Each components are connected to other components by using their relevant hostname like `redis`,`web`,`telephony`,`socket`,`db` through docker environment file or relevant configuration mentioned through service file for each component.

According to the installation change those components hostname to `127.0.0.1` or relevant IP Address/domain name. Otherwise those services may fail to start or won't work as expected.

Refer tools folder for each component installation and related service file and it's configuration adjustment.

### nginx

Webserver which we used to server our web application and also used for proxy for other web based request.

* Used for proxy web request
* Using upstream option able to load balancing multiple instance/IP.
* Able to do sticky connection per single upstream alone. Within upstream able to use same destination IP for further connection
, so that from same end-user IP request will go same destination IP which is configured on upstream.

Port Used:

- 80 - HTTP
- 443 - HTTPS
- 3232 - WebSocket - Proxy for Websocket port 3233(flexydial-websocket)
- 7444 - WSS for Freeswitch - Proxy for Actual Freeswitch 7443 port. SIP Over WebSocket - Ignored as of now due to dedicated freeswitch for users, campaign.
So comment this listener on nginx and connect directly to 7443 from Switch configuration.

### flexydial-app

It's Django App used for web page interactive application for agent/admin portal.
It's listening on 8001 port using *uwsgi module* which would accept connection from webserver.

* Able to run more than one instance to balance the load.
* No Sticky connection required.

Ports Used:
* 8001

Docker Image:
- vedakatta/flexydial-app

### flexydial-autodial
It's Django app with apscheduler to execute autodial algorithm and initiating dialling related jobs will be executed from this app.

Ports Used:
* None

Docker Image:
- vedakatta/flexydial-app

Used same base docker image of our app and startup command will be vary. *python manage.py autodial*

### flexydial-websocket
It's nodejs app and it would create listener for each type of dial method and will receive request from Freeswitch while executing dialplan.
And also it would be connected to dialer user using 3233 port.

Ports Used:
* 3233
* 8084 - SIP Session
* 8085 - Outbound Session Loop
* 8086 - Agent Workflow
* 8087 - Inbound

### flexydial-cdrd
Its django app which used to capture CDR data from freeswitch event and agent request.

Ports Used:
* None

Docker Image:
- vedakatta/flexydial-app

Used same base docker image of our app and start up command will be vary such as *python manage.py cdrd*

### flexydial-manager
It's django app which used to do back-end management activities such as background download/upload etc.

Ports Used:
* None

Docker Image:
- vedakatta/flexydial-app

Used same base docker image of our app and start up command will be vary such as *python manage.py manager*

### Redis
Its default redis application used for faster and intermediate storage for quciker retrieval instead of touching DB everytime.

Ports Used:
- 6379

DOcker Image:
- redis

### Postgresql
It's Database used on our application where as of now used PostgreSQL version 14 which is supported and tested.

Ports Used:
* 5432

Docker Image:
- postgres:14

### Freeswitch
Telephony Engine which our application using it complete calling workflow for end-user and connect customer.

Ports Used:
* 7443
* 5080 - External SIP

