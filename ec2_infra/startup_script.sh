#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
newgrp docker
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
ln -s /usr/bin/aws aws
aws ecr get-login-password --region us-west-1 |docker login --username AWS --password-stdin 192023623294.dkr.ecr.us-west-1.amazonaws.com
docker pull docker push 192023623294.dkr.ecr.us-west-1.amazonaws.com/stable-diffusion:xe2qeyrvrw2brea3
docker run -p 80:3000 --gpus all 192023623294.dkr.ecr.us-west-1.amazonaws.com/stable-diffusion:xe2qeyrvrw2brea3
