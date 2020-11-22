FROM python:3.8-slim
LABEL maintainer="Constantin Radulescu <constatin.r@gmail.com>"

ENV PYTHONPATH=$PYTHONPATH:/app/src/modules
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install curl -y

# Install docker
RUN curl -sSL https://get.docker.com/ | sh

# Copy SRC
WORKDIR /app/
COPY src /app/src/
COPY entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint

# Install modules

RUN pip3 install -r /app/src/requirements.txt

ENTRYPOINT ["/bin/entrypoint"]