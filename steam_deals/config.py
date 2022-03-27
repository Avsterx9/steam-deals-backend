from pathlib import Path
from typing import Final

from dynaconf import Dynaconf

from steam_deals.core import utils

ROOT_DIRECTORY: Final[Path] = Path(__file__).parent

settings = Dynaconf(
    envvar_prefix='STEAM_DEALS',
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    env_switcher='ENVIRONMENT_NAME',
)

VERSION: Final[str] = settings.get('VERSION', utils.get_version())
