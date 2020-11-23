import os


def aws_default_region():
    region = os.environ.get('AWS_DEFAULT_REGION')
    return region


def ecr_host():
    aws_account = os.environ.get('AWS_ACCOUNT')
    if aws_account:
        repository = (str(aws_account) + ".dkr.ecr." + aws_default_region() + ".amazonaws.com")
        return str(repository)
    else:
        exit(code=128)


def cloud():
    return str(os.environ.get('CLOUD'))


def db_path():
    path = os.environ.get('DB_PATH')
    return str(path)


def insert_db(name):
    try:
        f = open(db_path(), "a")
        f.write(name + "\n")
        f.close()
    except:
        pass
