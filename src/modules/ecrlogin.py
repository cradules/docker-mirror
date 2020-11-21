import base64
import os
import subprocess
import boto3


# Login to ECR AWS Function. This will use credentials from ENV or you credential files from ~/.aws/credentials
def login_docker_client_to_aws_ecr():
    # Create boto3 ECR client
    aws_default_region = os.environ.get('AWS_DEFAULT_REGION')
    ecr_client = boto3.client('ecr', region_name=aws_default_region)

    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']

    # Login via the docker sdk doesnt work so we're gonna go with this workaround
    command = 'docker login -u %s -p %s %s' % (username, password, registry)

    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.communicate()  # close p.stdout, wait for the subprocess to exit
