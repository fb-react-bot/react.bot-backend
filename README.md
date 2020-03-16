# react.bot-backend?
* This repository is for our react.bot backend! 
* It consists of two servers. One is for communicating with the client in real-time and the other is for inferencing user's voice.

# How to start this..
Now it will be working on a cloud server(http://35.221.251.166:80) until this week if you want to build this on your own, follow the below. 

1) Edit settings.py: 
```
HOST_URL = {your IP address}
```
2) Deploying a model API first and a socket server in a same host.
* the file "docker-compose.yaml" has configurations for two services: react_bot_backend_svc and react_bot_model_svc
* "docer-compose up" will build up all of the services. 

```bash
git clone https://github.com/fb-react-bot/react.bot-backend.git 
cd react.bot-backend
docker-compose up --build -d
``` 

# System Architecture 
![Image of System](https://github.com/fb-react-bot/react.bot-backend/blob/master/architecture.png)
