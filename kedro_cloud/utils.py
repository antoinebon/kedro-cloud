import logging
import shutil
from pathlib import Path
from typing import Sequence
import subprocess

from kedro.framework.project import settings
from kedro.framework.cli.utils import call


logger = logging.getLogger("kedro")


def get_plugin_config(env=None):
    config_loader = settings.CONFIG_LOADER_CLASS(
        settings.CONF_SOURCE, env=env, **settings.CONFIG_LOADER_ARGS
    )
    return config_loader.get("kedro_cloud*")["kedro_cloud"]


def copy_template_files(
    dest_path: Path,
    template_path: Path,
    template_files: Sequence[str],
):
    """
    If necessary copy files from a template directory into a dest directory.

    Args:
        dest_path: Destination path.
        template_path: Source path.
        template_files: Files to copy.
    """
    for file_ in template_files:
        dest = dest_path / file_
        if not dest.exists():
            src = template_path / file_
            shutil.copyfile(str(src), str(dest))
            logger.info(f"Creating `{dest}`")
        else:
            logger.info(f"{dest} already exists and won't be overwritten.")


def docker_aws_ecr_login(image_uri):
    region = image_uri.split(".")[3]
    pwd = f"aws ecr get-login-password --region {region}".split(" ")
    pwd = subprocess.run(pwd, check=True, capture_output=True)
    login = f"docker login --username AWS --password-stdin {image_uri}".split(" ")
    login = subprocess.run(login, input=pwd.stdout, capture_output=True)
    logger.info(f"Docker login status: {login.stdout.decode('utf-8').strip()}")


def kedro_docker_build(image):
    cmd = f"kedro docker build --image {image}".split(" ")
    call(cmd)


def docker_push(image):
    cmd = f"docker push {image}".split(" ")
    call(cmd)
