#!/bin/sh

# change locale
echo "Start installing language!"
apt-get install -y language-pack-ko
locale-gen ko_KR.UTF-8
echo "LC_ALL=ko_KR.utf8" > /etc/default/locale

# change timezone
timedatectl set-timezone Asia/Seoul


# restart ssh
systemctl restart sshd


# update docker-repository 
sudo apt-get -y update \
    && sudo apt-get remove -y docker docker-engine docker.io 

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - \
    && sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" 

# install docker 
sudo apt-get -y update \
    && sudo apt-get install -y docker-ce=5:19.03.4~3-0~ubuntu-bionic

# add user to docker
groupadd docker
usermod -aG docker "subhr1048"


# docker enable 
systemctl enable docker

# get docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && sudo chmod +x /usr/local/bin/docker-compose \
    && sudo wget \
        --output-document=/etc/bash_completion.d/docker-compose \
        "https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose" \
    && printf '\nDocker Compose installed successfully\n\n'
