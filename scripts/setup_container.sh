#! /usr/bin/bash

sudo apt update && sudo apt install -y git default-jdk python3 python3-pip wget curl tar parallel

cd $HOME

mkdir -p duality/tools

pushd duality/tools

# Install Maven
wget -O - https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz | tar xzf -
sudo ln -s $PWD/apache-maven-3.9.6/bin/* /usr/bin

# Install NVM
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install --lts
nvm use --lts

cd ..

git clone https://github.com/rongpan/RFixer.git

pushd RFixer

mvn install
sudo ln -s $PWD/*z3* /usr/lib/