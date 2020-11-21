import docker
import configparser
import dorepo
import misc


def run(file):
    # Create docker client
    docker_client = docker.from_env()

    # Read variables from config.ini. This implies that only config.ini should be modified for mirroring new images
    config = configparser.ConfigParser()
    config.read(file)

    # Iterate trough config.ini
    for section in config.sections():
        items = dict(config[section])  # Create dictionary from config.ini sections
        sr = items['source-repository']  # Create variable with the source from where the image will be pulled
        tag = items['tag']  # Create a variable with the image tag
        project = items['project']  # Create a variable with the target where the image will be pushed
        image = items['image']  # Create variable with then name and tag of the pulled image
        image_source = (sr + "/" + image + ":" + tag)  # Create variable for source image
        repository = (project + "/" + image)
        image_target = (
                    misc.ecr_repository() + "/" + project + "/" + image + ":" + tag)  # Create variable for source image

        try:
            docker_client.images.pull(image_source)  # Pull image from repository
            pull_image = docker_client.images.get(image_source)  # Read source image from localhost
            print('Successfully pulled image ' + image_source)
            pull_image.tag(image_target)  # Tag image with repository target name and tag
            print('Successfully tag image ', image_source, " to ", image_target, sep="")
            # Create repository if not exists
            dorepo.run(repository=repository)
            docker_client.images.push(image_target)  # Push image to ecr
            print('Successfully pushed image ', image_target, sep="")

        except ValueError:
            print(ValueError)
