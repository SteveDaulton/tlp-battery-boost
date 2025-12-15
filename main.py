"""MkDocs macros for project metadata.

Expose MkDocs macro variables derived from the project's `pyproject.toml`,
allowing automatic update of the app version number in the documentation.
"""

from __future__ import annotations
from pathlib import Path
import tomllib


def define_env(env):
    """Define MkDocs macro variables."""
    pyproject = Path(__file__).parent / "pyproject.toml"

    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)

    env.variables["app_version"] = data["project"]["version"]
