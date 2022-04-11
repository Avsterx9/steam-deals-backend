from pathlib import Path
from typing import Final

from dynaconf import Dynaconf
from starlette.templating import Jinja2Templates

from steam_deals.core import utils

ROOT_DIRECTORY: Final[Path] = Path(__file__).parent
ENV_SWITCHER: Final[str] = 'ENVIRONMENT_NAME'

templates = Jinja2Templates(directory=ROOT_DIRECTORY / 'core/templates')

settings = Dynaconf(
    envvar_prefix='STEAM_DEALS',
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    env_switcher=ENV_SWITCHER,
    env='DEVELOPMENT_LOCAL',
)

VERSION: Final[str] = settings.get('VERSION', utils.get_version())
