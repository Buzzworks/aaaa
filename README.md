Flexydial 6.0
====================================

Requirements:
-------------------------
- Any Recent Operating System ( Redhat / CentOS / Ubuntu ).
- Python3.8
- Docker CE Stable

Application Components
-------------------------

Each of these components mentioned below are able to run it same or different server.

- flexydial-app
- flexydial-autodial
- flexydial-cdrd
- flexydial-websocket
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

Refer tools folder for each component installation and related service file and it's configuration adjustment