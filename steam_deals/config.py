from pathlib import Path
from typing import Final

from dynaconf import Dynaconf

from steam_deals.core import utils

ROOT_DIRECTORY: Final[Path] = Path(__file__).parent
GIT_DIRECTORY: Final[Path] = ROOT_DIRECTORY.parent

settings = Dynaconf(
    envvar_prefix='STEAM_DEALS',
    settings_files=[GIT_DIRECTORY / 'settings.toml', GIT_DIRECTORY / '.secrets.toml'],
    environments=True,
    load_dotenv=True,
    dotenv_path=GIT_DIRECTORY / '.env',
)

VERSION: Final[str] = settings.get('VERSION', utils.get_version())
