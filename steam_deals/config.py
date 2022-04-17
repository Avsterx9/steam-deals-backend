from pathlib import Path
from typing import Final

import git
from dynaconf import Dynaconf
from starlette.templating import Jinja2Templates

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


def get_version() -> str:
    repo = git.Repo(search_parent_directories=True)
    # if there are any changes (staged, tracked or untracked) do not refer the SHA of last commit
    return (
        'UNCOMMITTED'
        if repo.index.diff(None) or repo.index.diff('HEAD') or repo.untracked_files
        else repo.head.object.hexsha
    )


VERSION: Final[str] = settings.get('VERSION', get_version())
