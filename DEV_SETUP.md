# Flexydial-6 Dev 

## Prerequisites:
Prerequisites to do any new dev setup or Ip changes occured.

```
echo APP_HOST=enter_ip_of_app >> /etc/environment
echo REDIS_HOST=enter_ip_of_app >> /etc/environment
echo DB_HOST=enter_ip_of_app >> /etc/environment
echo SOCKET_HOST=enter_ip_of_app >> /etc/environment
echo TELEPHONY_HOST=enter_ip_of_app >> /etc/environment
echo APP_PATH= >> /etc/environment 
example : echo APP_PATH=/home/buzzworks/flexydial >> /etc/environment
echo ENV=DEV >> /etc/environment
```

## Installation Steps/Hints:
```
sudo su
```
```
cd tools/
```
```
chmod -R +x *
```
```
./docker-install.sh # to install Docker in the system.
```
```
cd redis/
```
```
./docker-instance.sh # to create redis container
```
- To Create postgres container.
```
cd .. && cd postgres && ./docker-instance.sh # to create postgres container
```
- To create Websocket image
```
cd ../../fs-dialplan/ && ./dev_setup.sh # to create websocket image locally
```
- To Create WebSocket container
```
cd ../tools/websocket/ && ./docker-instance.sh # to create websocket container
```
- To Create App Local Image
```
cd ../../ && ./dev-setup.sh # to create app image locally
```
```
cd tools/app/
```
- Modify docker-instance.sh REPLACE Mention WebSocket Server IP address/domain name REPLACE Mention Telephony Server IP address/domain name
Save the file
- To Create Certificates
```
./flexycrt.sh
```
- To Create App and Nginx Container
```
./docker-instance.sh # to create app,nginx container
```
- To create Freeswitch installation, cdr and autodial daemons
```
cd ../freeswitch/ && ./instance.sh
```


## Imp Docker Commands:
-To get the all the docker process list
```
sudo docker ps
```
- To get the logs
```
sudo docker logs <container-name> -f
```

## Latest Updates related to Rabbitmq:
- Rabbitmq setup
```
echo RABBITMQ_HOST=enter_rabbitmq_host_ip >> /etc/environment
```
```
cd tools/rabbitmq/
```
```
./docker-instance.sh # to create rabbitmq server and worker
```