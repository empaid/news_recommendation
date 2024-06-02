sudo su -
yum install git -y
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
amazon-linux-extras install java-openjdk11 -y
yum install jenkins -y
sudo su -
systemctl enable jenkins
systemctl start jenkins
systemctl status jenkins
cat /var/lib/jenkins/secrets/initialAdminPassword
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
docker --version
sudo usermod -a -G docker $(whoami)
newgrp docker

DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
cat /var/lib/jenkins/secrets/initialAdminPassword
