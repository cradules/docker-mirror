# ECR Mirror Images

This small python scrip will help you to mirror images from docker hub to your ECR private docker registry.

# Requirements

- Create filed config.ini in src folder with the form:

```ini
[reposiotry/imagename]
image = "image name" 
tag = "image tag"
source-repository = "source repository"
target-repository = "target repository"
region = "aws region"

[reposiotry2/imagename2]
image = "image name"
tag = "image tag"
source-repository = "source repository"
target-repository = "target repository"
region = "aws region"
```
- Export on the environment that will run the docker image next env objects:

```shell script
AWS_DEFAULT_REGION="AWS region"
AWS_ACCESS_KEY_ID="AWS access key"
AWS_SECRET_ACCESS_KEY="AWS secret key"
CLOUD="Cloud name" -  Ex: AWS, AZURE, GOOGLE (NOTE: For the moment the solution supports on AWS)
AWS_ACCOUNT="AWS account ID"
```



## User Guide
### Build image
```shell script
docker build -t docker-mirror .
```

### Run docker mirror on local machine:

```shell script
docker run  --privileged -v ${HOME}/db:/db -e AWS_DEFAULT_REGION=<aws region> -e AWS_ACCOUNT=<aws account> -e CLOUD=AWS -e DB_PATH=/db/repository.db -e AWS_ACCESS_KEY_ID=<aws key id> -e AWS_SECRET_ACCESS_KEY=<aws accces key> docker-mirror

```