import os
import boto3


def run():
    # Create boto3 ECR client
    aws_default_region = os.environ.get('AWS_DEFAULT_REGION')
    ecr_client = boto3.client('ecr', region_name=aws_default_region)
    response = ecr_client.create_repository(
        repositoryName='project-a/nginx-web-app',
    )

    print(response)