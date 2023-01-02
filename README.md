# Kedro + Cloud Integration

Kedro plugin for deploying containerized Kedro application on cloud infrastructures such as AWS Sagemaker
This plugin is usefull when you want to run Kedro on a single temporary cloud machine, such as the ones provided by AWS Sagemaker


## What will you get with this integration?

* AWS Sagemaker integration:
    * Automated build and deployment of Kedro application image on AWS ECR
    * Automated run of Kedro application using Sagemaker Processing job


## Get started

On the command line:

```bash
pip install kedro-cloud
```

In your Kedro project directory (this will initialize an empty configuration file named
`kedro_cloud.yml` in the desired configuration environment)

```bash
kedro cloud init --env {env}
```

## AWS Sagemaker

In order to run a Kedro docker image on AWS Sagemaker you first need to
configure the following 2 infrastructure components:

1. An ECR Repository where kedro-cloud will push the docker image of your Kedro
   application
2. An execution role for the Sagemaker Processing job, which should have
   the necessary priviledges to run a Sagemaker job (such as `AmazonSageMakerFullAccess`),
   and in case your data is on S3, the role should also have access to the
   required S3 buckets (such as `AmazonS3FullAccess`)


Once you have the infrastructure above in place, copy the `image_uri` for the
ECR repository and the `role_arn` for the Sagemaker job in `kedro_cloud.yml`


Kedro-cloud requires that you have [AWS CLI](https://aws.amazon.com/cli/)
installed, so make sure you have it installed before running kedro-cloud
sagemaker integration


After that, running your Kedro application on AWS Sagemaker is as easy as:
```bash
kedro cloud sagemaker run --pipeline {pipeline} --env {env}
```

## Other cloud providers

AWS Sagemaker is the only integration supported at the moment. Feel free to
submit a PR if you wish to extent this plugin
