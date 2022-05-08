import logging
from typing import Final
from typing import List
from typing import Union

from fastapi import APIRouter
from fastapi import Query
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND

from steam_deals.core import apps
from steam_deals.core import schemas
from steam_deals.core import utils
from steam_deals.core.exception import HTTPException

log = logging.getLogger('steam_deals')

apps_router = APIRouter()

DETAILED_QUERY_DESC: Final[str] = (
    'Responds with AppBase or AppDetailed objects. ' + 'There is a lower limit when querying for detailed apps.'
)


@apps_router.get(
    path='/apps/id/{appid}',
    response_model=Union[schemas.AppDetailed, schemas.AppBase],
    tags=['apps'],
    description='Get information about app by provided steam `appid`.',
    responses=utils.create_status_responses({HTTP_404_NOT_FOUND: 'When there is no app with given `app_id`'}),
)
def read_app(app_id: int, detailed: bool = True):
    app_base = apps.get_base_app(app_id=app_id)

    if not app_base:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Could not find app with app_id of {app_id}')

    if not detailed:
        return app_base

    app_detailed = apps.get_detailed_app(app_base=app_base)

    if not app_detailed:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Could not find app with app_id of {app_id}')

    return app_detailed


@apps_router.get(
    path='/apps/top100in2weeks',
    response_model=List[schemas.AppBase],
    tags=['apps'],
    description='Get `N first` apps from `top100 in 2weeks` sorted by `CCU` yesterday.',
)
def read_n_apps_of_top100_in_2_weeks(skip: int = 0, amount: int = 5):
    return apps.get_top100_in_2weeks_apps(skip=skip, amount=amount)


@apps_router.get(
    path='/apps/top100in2weeks/random',
    response_model=Union[List[schemas.AppDetailed], List[schemas.AppBase]],
    tags=['apps'],
    description='Get `N random` apps from `top100 in 2weeks` by `CCU` yesterday.',
    responses=utils.create_status_responses({HTTP_400_BAD_REQUEST: 'When requested amount of apps was too large.'}),
)
def read_n_random_apps_of_top100_in_2_weeks(
    amount: int = 5,
    detailed: bool = Query(False, description=DETAILED_QUERY_DESC),
):
    limit_detailed: Final[int] = 10

    if not detailed:
        return apps.get_top100_in_2weeks_random_apps(amount=amount)

    if amount > limit_detailed:
        raise HTTPException(
            status_code=400,
            detail=f'Requested {amount} apps but {limit_detailed} is the actual limit when querying for detailed app',
        )

    return apps.get_top100_in_2weeks_random_apps_detailed(amount=amount)
