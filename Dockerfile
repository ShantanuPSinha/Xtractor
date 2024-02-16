# Use an existing Docker image as a base
FROM ubuntu:latest

# Install necessary dependencies
RUN apt update && apt install -y \
    git default-jdk python3 python3-pip wget curl tar

RUN wget -O - https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz | tar xzf -

# Install Node Version Manager (NVM)
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Install Node.js

RUN nvm install node

# Clone the repository from GitHub
RUN git clone <GitHub repository URL>

# Copy all scripts into the container
COPY ./scripts /app/scripts

# Set working directory
WORKDIR /app

# Specify the command to run when the container starts
CMD ["python", "main_script.py"]
