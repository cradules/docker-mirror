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
AWS_DEFAULT_REGION="region"
AWS_ACCESS_KEY_ID="access key"
AWS_SECRET_ACCESS_KEY="secret key"
```