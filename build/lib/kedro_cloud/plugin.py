""" Kedro plugin for packaging a project with cloud """
from pathlib import Path
import logging

import click

from kedro.framework.cli.utils import KedroCliError, call, forward_command
from kedro.framework.project import settings

from .utils import (
    copy_template_files,
)

logger = logging.getLogger(__name__)


@click.group(name="cloud")
def cloud():
    """Kedro plugin for deploying kedro in the cloud"""
    pass


@cloud.command(name="init")
def init():
    """Initialize a configuration file for the project"""
    project_path = Path.cwd()
    template_path = Path(__file__).parent / "template"

    copy_template_files(
        project_path / settings.CONF_SOURCE / "base",
        template_path,
        ["kedro_cloud.yml"],
    )


@cloud.group(name="sagemaker")
def sagemaker():
    pass


@sagemaker.command(name="deploy")
def deploy():
    pass


@sagemaker.command(name="run", context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_context
def sagemaker_run(ctx):
    config_loader = settings.CONFIG_LOADER_CLASS(settings.CONF_SOURCE, **settings.CONFIG_LOADER_ARGS)
    plugin_config = config_loader.get("kedro_cloud")
    print(plugin_config)
    print(ctx.args)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    cloud()
