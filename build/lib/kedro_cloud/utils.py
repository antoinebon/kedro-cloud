import logging
import shutil
from pathlib import Path
from typing import Sequence

logger = logging.getLogger(__name__)


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
