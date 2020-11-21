import boto3
import misc


def check_repository(repository):
    try:
        # Create boto3 ECR client
        ecr_client = boto3.client('ecr', region_name=misc.aws_default_region())
        response = ecr_client.list_images(
            repositoryName=repository,
        )
        return response

    except:
        pass


def run(repository):
    if not check_repository(repository):
        # Create boto3 ECR client
        ecr_client = boto3.client('ecr', region_name=misc.aws_default_region())
        response = ecr_client.create_repository(
            repositoryName=repository,
        )
        return response
    else:
        print('Repository {0} exists on host {1}'.format(repository, misc.ecr_host()))
