import click
import inspect
import pkgutil
import sys

from kubernaut.util import *
from kubernaut.config.model import Config
from kubernaut.model import *
from kubernaut.backend import Backend
from ruamel.yaml import YAML
from typing import Optional

model_classes = inspect.getmembers(sys.modules["kubernaut.model"], inspect.isclass)

yaml = YAML(typ='safe')
yaml.register_class(ClaimSpec)

version = "unknown"
try:
    version = pkgutil.get_data('kubernaut', 'version.txt').decode("utf-8")
except FileNotFoundError:
    pass

__version__ = version


class KubernautContext:

    def __init__(self, config: Config):
        self.config = config

    def get_backend(self, name: Optional[str] = None, fail_if_missing: bool = True) -> Optional[Backend]:
        result = None
        if name is None:
            result = self.config.current_backend
        else:
            result = self.config.get_backend(name)

        if result is None and fail_if_missing:
            msg = strip_margin("""
            |
            | Kubernaut is not configured to communicate with a backend!
            |
            | Use `kubernaut config backend --help` to learn how to manage backends.
            |
            | Note, if you are migrating from kubernaut v1, do this:
            |
            | 1. Grab your legacy JWT from `~/.config/kubernaut/config.json`
            | 2. `kubernaut config backend create --url="https://next.kubernaut.io" --name="v2" --activate <token>`
            |
            """)

            raise click.ClickException(msg)
        else:
            return result
