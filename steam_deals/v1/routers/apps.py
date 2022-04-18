import datetime
import logging
import random
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from typing import Final
from typing import List
from typing import Optional
from typing import Set

import requests
from fastapi import APIRouter
from requests.exceptions import SSLError

from steam_deals.core import schemas
from steam_deals.core.exception import HTTPException

log = logging.getLogger("steam_deals")

apps_router = APIRouter()


@apps_router.get(
    path='/apps/2weeks/random',
    response_model=List[schemas.AppBase],
    tags=['apps'],
)
def read_random_apps(amount: int = 5):
    limit = 10
    # request = requests.get(url='http://api.steampowered.com/ISteamApps/GetAppList/v2')
    # request = requests.get(url='https://steamspy.com/api.php?request=top100in2weeks')
    # result = request.json()  # ['applist']['apps']
    if amount > limit:
        raise HTTPException(status_code=400, detail=f'Requested {amount} apps but {limit} is the actual limit')

    return random_apps(amount=amount)


def random_apps(amount: int) -> List[schemas.AppBase]:
    apps = []

    while (diff := amount - sum(1 for i in apps if i is not None)) > 0:
        excluded_app_ids = {app.steam_appid for app in apps if app is not None}
        randomized_app_ids = get_random_top100_2weeks_app_ids(amount=diff, excluded=excluded_app_ids)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_detailed_app_schema, app_id) for app_id in randomized_app_ids]

            for future in as_completed(futures):
                apps.append(future.result())

    apps = list(filter(None, apps))
    assert len(apps) == amount
    return apps


def get_detailed_app_schema(app_id: int) -> Optional[schemas.AppBase]:
    # pylint: disable=too-many-locals

    url: Final[str] = 'https://store.steampowered.com/api/appdetails'

    result = get_request(url=url, params={'appids': app_id, 'cc': 'en'})[app_id]
    if not result['success']:
        log.warning(f'Error while getting: {app_id} Data: {result}')
        return None

    app = result['data']
    app_type = app.get('type', None)
    name = app.get('name', None)
    developers = app.get('developers', [])
    publishers = app.get('publishers', [])
    short_description = app.get('short_description', None)
    is_free = app.get('is_free', None)

    price = None
    if price_overview := app.get('price_overview', None):
        currency = price_overview.get('currency', None)
        value = float(price_overview.get('final', None) / 100)
        price = {currency: value}

    screenshots_raw = app.get('screenshots', [])
    screenshots = []
    for screenshot in screenshots_raw:
        if path := screenshot.get('path_thumbnail', None):
            screenshots.append(path)

    release_date_raw = app.get('release_date', None)
    release_date = None
    if date := release_date_raw.get('date', None):
        release_date = datetime.datetime.strptime(date, "%d %b, %Y")

    values = {
        'steam_appid': app_id,
        'app_type': app_type,
        'name': name,
        'header_image': f'https://steamcdn-a.akamaihd.net/steam/apps/{app_id}/header.jpg',
        'developers': developers,
        'publishers': publishers,
        'screenshots': screenshots,
        'short_description': short_description,
        'is_free': is_free,
        'price': price,
        'release_date': release_date,
    }

    return schemas.AppBase(**values)


def get_random_top100_2weeks_app_ids(amount: int, excluded: Optional[Set[int]] = None) -> List[int]:
    result = get_request(url='https://steamspy.com/api.php?request=top100in2weeks')
    app_ids = set(result.keys())

    if amount > len(app_ids):
        raise HTTPException(status_code=400, detail=f'Requested {amount} apps but {len(app_ids)} is the maximum amount')

    return random.sample(population=app_ids - excluded, k=amount)


def get_request(url: str, params: Optional[dict] = None, attempts: int = 3) -> dict:
    """Return json-formatted response of a get request using optional parameters."""

    if attempts <= 0:
        raise HTTPException(status_code=503, detail='External service is unavailable. Please try again later.')

    try:
        response = requests.get(url=url, params=params)
    except SSLError as exception:
        log.warning(f'SSL Error: {exception}')
        log.warning(f'Attempts left: {attempts}. No response, waiting 3 seconds...')
        time.sleep(3)
        log.debug('Retrying...')

        return get_request(url=url, params=params, attempts=attempts - 1)

    if response:
        log.debug(f'URL: {create_url_with_params(url=url, params=params)} Response: {response.status_code}')
        return response.json()

    log.warning(f'Attempts left: {attempts}. No response, waiting 3 seconds...')
    time.sleep(3)
    log.debug('Retrying...')
    return get_request(url=url, params=params, attempts=attempts - 1)


def create_url_with_params(url: str, params: Optional[dict] = None) -> str:
    if not params:
        return url
    return f'{url}?{urllib.parse.urlencode(params)}'
