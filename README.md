# Docker Mirror Image

## Description

This is solution that will help you to mirror docker images form a repository to another.
DMI ( docker mirror Images) was build to overcome the the situation where an environment ( like kubernetes) need images from
docker hub, but as we know since 2 of November 2020, docker hub has implemented a [rate limit](https://www.docker.com/increase-rate-limits#:~:text=The%20rate%20limits%20will%20be,the%20six%20hour%20window%20elapses.).

At this moment the solution support just AWS ECR mirroring and support next tasks:
- pull images from docker hub
- re-tag images
- create new repository in AWS ECR
- push images to newly created AWS ECR
- keep track of the mirror images
- refresh mirrored images if is specified.


# Requirements
The solution is working around a provided config.ini file where you need to specify the repository/images that needs to be mirrored
- Create filed config.ini in src folder with the form:

```ini
[DEFAULT]
refresh = 1w

[aws/proxyv2]
image = proxyv2
tag = 1.7.0
source-repository = istio
project = istio

[aws/mixer]
image = mixer
tag = 1.7.0
source-repository = istio
project = istio
```
- Export for the environment that will used by docker container next env objects:

```shell script
AWS_DEFAULT_REGION="AWS region"
AWS_ACCESS_KEY_ID="AWS access key"
AWS_SECRET_ACCESS_KEY="AWS secret key"
CLOUD="Cloud name" -  Ex: AWS, AZURE, GOOGLE (NOTE: For the moment the solution supports on AWS)
AWS_ACCOUNT="AWS account ID"
```



## User Guide
-  Build image
```shell script
docker build -t docker-mirror .
```

- Run docker mirror on local machine:

```shell script
docker run  --privileged -v <full path to>/db:/db -v <full pato to>/config.ini:/app/src/config.ini-e AWS_DEFAULT_REGION=<aws region> -e AWS_ACCOUNT=<aws account> -e CLOUD=AWS -e DB_PATH=/db/repository.db -e AWS_ACCESS_KEY_ID=<aws key id> -e AWS_SECRET_ACCESS_KEY=<aws accces key> docker-mirror

```

- Scheduler. DMI is offering the possibility to refresh the mirrored imaged to a given time interval. 
The supported intervals are:
    - minutes
    - days
    - weeks

The refresh interval is given by config.ini on [DEFAULT] section and supports next values:
- 0 - will disable refresh
- [n]m - minutes. Where n is a positive integer
- [n]d - days.  Where n is a positive integer
- [n]w - weeks. Where n is a positive integer


## HELM

Requirements:
- AWS
    - Create secret for AWS ACCESS on the namespace where your are deploying the chart
    ```shell script
    kubectl create secret generic  aws-dmi-secret \
    --from-literal=AWS_ACCESS_KEY_ID=<aws-access-key> \
    --from-literal=AWS_SECRET_ACCESS_KEY='<aws-secret-access-id>'
    --from-literal=AWS_ACCOUNT='<aws-account-id>'
    ```

        Note: On AWS EKS cluster if the cluster has ECR policy attached the secrets should not be necessary. 
        This case is not tested yet. Soon I will test I will modify the chart so the secretes to be optionally.  

-  Environment Variables:
    - CLOUD: "cloud provider"  AWS, AZURE, GKE ( for the moment only AWS is supported)
    - DB_PATH: "/db/file-name"
    - AWS_DEFAULT_REGION: "aws-region"


### TODO:
~~- Implement scheduler
    - The scheduler to be dictated by the user. 
      Ex: 
      - To refers mirrored images every day - refresh = 1d
      - To refers mirrored every 1 week - refresh = 1w .. and so on.
      - To refresh mirrored images never - refresh = 0 
      - Implement helm chart so the DMI can run inside kubernetes cluster.~~
- Implement support for others Cloud providers:
  - Google
  - Azure
- Implement support to mirror from Cloud to cloud
- Implement support to mirror images from sources that require authentication.
- Check Readme.md
