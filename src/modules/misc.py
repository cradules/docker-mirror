import os


def aws_default_region():
    region = os.environ.get('AWS_DEFAULT_REGION')
    return region


def ecr_host():
    aws_account = os.environ.get('AWS_ACCOUNT')
    if aws_account:
        repository = (str(aws_account) + ".dkr.ecr.eu-central-1.amazonaws.com")
        return str(repository)
    else:
        exit(code=128)


def cloud():
    return str(os.environ.get('CLOUD'))
