import boto3
import dmmisc


def check_repository(repository):
    try:
        # Create boto3 ECR client
        ecr_client = boto3.client('ecr', region_name=dmmisc.aws_default_region())
        response = ecr_client.list_images(
            repositoryName=repository,
        )
        return response

    except:
        pass


def create_ecr(repository):
    if not check_repository(repository):
        # Create boto3 ECR client
        ecr_client = boto3.client('ecr', region_name=dmmisc.aws_default_region())
        response = ecr_client.create_repository(
            repositoryName=repository,
        )
        print(response)
    else:
        print('Repository {0} exists on host {1}'.format(repository, dmmisc.ecr_host()))
