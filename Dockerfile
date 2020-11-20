FROM python:3.7-stretch
LABEL maintainer="Constantin Radulescu <constatin.r@gmail.com>"



# Install docker
RUN curl -sSL https://get.docker.com/ | sh

# Copy SRC
WORKDIR /app
COPY src /app

# Install modules

RUN pip3 install -r /app/requirements.txt