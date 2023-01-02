""" Kedro plugin for packaging a project with cloud """
from pathlib import Path
import logging

import click
from sagemaker.processing import Processor

from kedro.framework.cli.utils import KedroCliError, call, forward_command, env_option
from kedro.framework.cli.project import PIPELINE_ARG_HELP
from kedro.framework.project import settings

from .utils import (
    copy_template_files,
    get_plugin_config,
    docker_aws_ecr_login,
    kedro_docker_build,
    docker_push,
)

logger = logging.getLogger("kedro")


@click.group(name="Cloud")
def commands():
    """Kedro plugin for deploying kedro in the cloud"""
    pass


@commands.group(name="cloud")
def cloud_group():
    pass


@cloud_group.command(name="init")
@env_option(
    default="local", help="The config environment to put the template configuration in"
)
def init(env):
    """Initialize a configuration file for the project"""
    project_path = Path.cwd()
    template_path = Path(__file__).parent / "template"

    dest = project_path / settings.CONF_SOURCE / env
    dest.mkdir(parents=True, exist_ok=True)
    copy_template_files(
        dest,
        template_path,
        ["kedro_cloud.yml"],
    )


@cloud_group.group(name="sagemaker")
def sagemaker_group():
    pass


@sagemaker_group.command(name="deploy")
@env_option(default="local")
def deploy(env):
    """
    Containerize the project with kedro-docker,
    Authenticate docker against AWS ECR
    Push the container to AWS ECR
    """
    config = get_plugin_config(env)["aws"]["sagemaker"]
    image_uri = config["image_uri"]
    kedro_docker_build(image_uri)
    docker_aws_ecr_login(image_uri)
    docker_push(image_uri)


@forward_command(sagemaker_group, "run")
@env_option(default="local")
@click.option(
    "--pipeline", "-p", type=str, default="__default__", help=PIPELINE_ARG_HELP
)
@click.option(
    "--job-name", "-n", type=str, default=None, help="Name for the sagemeker job"
)
@click.option(
    "--deploy/--no-deploy",
    "deploy_flag",
    default=True,
    show_default=True,
    help="Build the docker image for the project using kedro-docker and push to AWS ECR",
)
@click.pass_context
def sagemaker_run(ctx, args, pipeline, env, job_name, deploy_flag, **kwargs):
    config = get_plugin_config(env)["aws"]["sagemaker"]
    job_name = pipeline if job_name is None else job_name
    base_job_name = f"kedro-{job_name}-{env}"
    base_job_name = base_job_name.replace("__", "").replace("_", "-").replace(".", "-")
    processor = Processor(
        image_uri=config["image_uri"],
        role=config["role_arn"],
        instance_count=1,
        instance_type=config["instance_type"],
        base_job_name=base_job_name,
    )

    if deploy:
        ctx.invoke(deploy, env=env)

    cmd = ["kedro", "run", "--pipeline", pipeline, "--env", env] + list(args)
    processor.run(arguments=cmd)
