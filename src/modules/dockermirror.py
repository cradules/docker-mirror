import configparser
import docker
import dmecr
import dmecrlogin
import dmmisc
from datetime import date, datetime


def run():
    # Create docker client
    docker_client = docker.from_env()
    # Read variables from config.ini. This implies that only config.ini should be modified for mirroring new images
    config = configparser.ConfigParser()
    config.read('config.ini')
    if dmmisc.cloud() == 'AWS':
        dmecrlogin.login_docker_client_to_aws_ecr()  # Login to ECR
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    day = today.strftime("%B %d, %Y")
    print(day + " " + current_time)

    # Iterate trough config.ini
    for section in config.sections():
        items = dict(config[section])  # Create dictionary from config.ini sections
        sr = items['source-repository']  # Create variable with the source from where the image will be pulled
        tag = items['tag']  # Create a variable with the image tag
        project = items['project']  # Create a variable with the target where the image will be pushed
        image = items['image']  # Create variable with then name and tag of the pulled image
        image_source = (sr + "/" + image + ":" + tag)  # Create variable for source image
        repository = (project + "/" + image)

        # Check Cloud type
        image_target = ""
        if dmmisc.cloud() == 'AWS':
            image_target = (dmmisc.ecr_host() + "/" + project + "/" + image + ":" + tag)

        open(dmmisc.db_path(), 'a').close()  # Initiate DB empty file ( is necessary to avoid other complications)

        # Check if "image_source" repo/image is present on DB file. If not pull the image
        try:
            with open(dmmisc.db_path()) as string:
                if image_source not in string.read():
                    docker_client.images.pull(image_source)  # Pull image from repository
                    dmmisc.insert_db(image_source)
                else:
                    print('Image {} present on repository.db file'.format(image_source))
        except ValueError:
            print(ValueError)

        # Create ECR repository on AWS if not exists
        try:
            dmecr.create_ecr(repository=repository)
        except ValueError:
            print(ValueError)

        # Check if "image_target" repo/image is present on DB file. If not pull the image
        try:
            with open(dmmisc.db_path()) as string:
                if image_target not in string.read():
                    pull_image = docker_client.images.get(image_source)  # Read source image from localhost
                    print('Successfully pulled image ' + image_source)
                    pull_image.tag(image_target)  # Tag image with repository target name and tag
                    print('Successfully tag image ', image_source, " to ", image_target, sep="")
                    dmmisc.insert_db(image_target)
                    docker_client.images.push(image_target)  # Push image to ecr
                    print('Successfully pushed image ', image_target, sep="")
                    docker_client.images.remove(image_source, image_target)
                    print('Successfully clean-up local storage')
                else:
                    print('Image {} present on repository.db file'.format(image_source))
        except ValueError:
            print(ValueError)
