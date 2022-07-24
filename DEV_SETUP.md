echo APP_PATH=<currentAPPdirectory> >> /etc/environment
example :
    echo APP_PATH=/home/buzzworks/flexydial >> /etc/environment

echo ENV=DEV >> /etc/environment
    
1. sudo su
2. cd tools/
3. chmod -R  +x *
4. ./docker-install.sh # to install Docker in the system.
5. cd redis/
6. ./docker-instance.sh # to create redis container
7. cd .. && cd postgres && ./docker-instance.sh # to create postgres container
8. cd ../../fs-dialplan/ && ./dev_setup.sh # to create websocket image locally
9. cd ../tools/websocket/ && ./docker-instance.sh # to create websocket container
10. cd ../../ && ./dev-setup.sh # to create app image locally
11. cd tools/app/ 
12. modify docker-instance.sh 
REPLACE Mention WebSocket Server IP address/domain name
REPLACE Mention Telephony Server IP address/domain name
13. Save the file
14. ./docker-instance.sh # to create app,nginx container
15. cd ../freeswitch/ && ./instance.sh
