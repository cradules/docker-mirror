import base64
import docker
import configparser
import logging
import sys
import subprocess32 as subprocess
import boto3
import os

# Log information to stdout. Change log level from "root.setLevel"
root = logging.getLogger()
root.setLevel(logging.INFO)  # Here you can change the log level

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# Create docker client
docker = docker.from_env()

# Create boto3 ECR client
aws_default_region = os.environ.get('AWS_DEFAULT_REGION')
ecr_client = boto3.client('ecr', region_name=aws_default_region)

# Read variables from config.ini. This implies that only repository.ini should be modified for mirroring new images
config = configparser.ConfigParser()
config.read("config.ini")


# Login to ECR AWS Function. This will use credentials on ENV or you credential files from ~/.aws/credentials
def login_docker_client_to_aws_ecr():
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']

    # Logging in via the docker sdk doesnt work so we're gonna go with this workaround
    command = 'docker login -u %s -p %s %s' % (username, password, registry)

    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.communicate()  # close p.stdout, wait for the subprocess to exit


# Login to ECR
login_docker_client_to_aws_ecr()

# Iterate trough config.ini
for section in config.sections():
    items = dict(config[section])  # Create dictionary from config.ini sections
    sr = items['source-repository']  # Create variable with the source from where the image will be pulled
    tag = items['tag']  # Create a variable with the image tag
    tr = items['target-repository']  # Create a variable with the target where the image will be pushed
    image = items['image']  # Create variable with then name and tag of the pulled image
    image_source = (sr + "/" + image + ":" + tag)  # Create variable for source image
    image_target = (tr + "/" + image + ":" + tag)  # Create variable for source image

    try:
        docker.images.pull(image_source)  # Pull image from repository
        pull_image = docker.images.get(image_source)  # Read source image from localhost
        print('Successfully pulled image ' + image_source)
        pull_image.tag(image_target)  # Tag image with repository target name and tag
        print('Successfully tag image ', image_source, " to ", image_target, sep="")
        docker.images.push(image_target)  # Push image to ecr
        print('Successfully pushed image ', image_target, sep="")

    except ValueError:
        print(ValueError)
