## what is react.bot-backend?
* this repository is for our react.bot backend servers! 
* it consists of two servers. One is for communicating with the client in real-time and the other is for inferencing user's voice.

## How to start this..
* Deploying a model API first and a socket server.
* the file "docker-compose.yaml" has configurations for two services: react_bot_backend_svc and react_bot_model_svc

```bash
git clone https://github.com/fb-react-bot/react.bot-backend.git 
cd react.bot-backend
docker-compose up --build -d
``` 

## System Architecture 
![Image of System](https://octodex.github.com/images/yaktocat.png)
