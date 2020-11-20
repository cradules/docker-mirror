FROM python:3.7-stretch
LABEL maintainer="Constantin Radulescu <constatin.r@gmail.com>"



# Install docker
RUN curl -sSL https://get.docker.com/ | sh

# Copy SRC
WORKDIR /app
COPY src /app
COPY entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint

# Install modules

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["/bin/entrypoint"]