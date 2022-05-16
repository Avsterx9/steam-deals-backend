import logging
import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from typing import Final
from typing import List
from typing import Optional
from typing import Set

from steam_deals.core import schemas
from steam_deals.core import utils
from steam_deals.core.exception import HTTPException
from steam_deals.core.requests import get_request

log = logging.getLogger('steam_deals')

URL_STEAMSPY: Final[str] = 'https://steamspy.com/api.php'
URL_STEAM_POWERED_APP_DETAILS: Final[str] = 'https://store.steampowered.com/api/appdetails'
URL_HEADER_IMAGE: Final[str] = 'https://steamcdn-a.akamaihd.net/steam/apps/:app_id:/header.jpg'
URL_SEARCH_APPS: Final[str] = 'https://steamcommunity.com/actions/SearchApps'


def create_app_base_object(app: dict, index: Optional[int] = None) -> schemas.AppBase:
    # pylint: disable=too-many-locals

    steam_appid = app['appid']
    name = app.get('name', None)

    developers = []
    if developer := app.get('developer', None):
        developers = developer.split(',')

    publishers = []
    if publisher := app.get('publisher', None):
        publishers = publisher.split(',')

    positive = app.get('positive', None)
    negative = app.get('negative', None)

    positive_percent = None
    if positive and negative:
        positive_percent = round(positive / (positive + negative) * 100, 2)

    owners = {}
    if owners_raw := app.get('owners', None):
        lower, upper = owners_raw.replace(',', '').split(' .. ')
        owners = {'lower_bound': int(lower), 'upper_bound': int(upper)}

    ccu_yesterday = app.get('ccu', None)

    price = {}
    if price_raw := app.get('price', None):
        price['final'] = int(price_raw) / 100

    if price_initial := app.get('initialprice', None):
        price['initial'] = int(price_initial) / 100

    if price.get('initial', None) and price.get('final', None):
        price['discount'] = round((1 - price['final'] / price['initial']) * 100, 2)

    container = {
        'steam_appid': steam_appid,
        'name': name,
        'index': index,
        'ccu_yesterday': ccu_yesterday,
        'header_image': URL_HEADER_IMAGE.replace(':app_id:', str(steam_appid)),
        'developers': developers,
        'publishers': publishers,
        'positive': positive,
        'negative': negative,
        'positive_percent': positive_percent,
        'owners': owners,
        'price': price,
    }
    return schemas.AppBase(**container)


def get_top100_in_2weeks_apps(skip: int, amount: int) -> List[schemas.AppBase]:
    result = get_request(url=URL_STEAMSPY, params={'request': 'top100in2weeks'})
    playtime_avg_sorted_app_ids = sorted(result, key=lambda key: result[key]['ccu'], reverse=True)[skip : amount + skip]

    return [
        create_app_base_object(app=result[app_id], index=index)
        for index, app_id in enumerate(playtime_avg_sorted_app_ids)
    ]


def get_top100_in_2weeks_random_apps(amount: int, excluded_app_ids: Optional[Set[int]] = None) -> List[schemas.AppBase]:
    apps = get_top100_in_2weeks_apps(skip=0, amount=100)

    if amount > len(apps):
        raise HTTPException(status_code=400, detail=f'Requested {amount} apps but {len(apps)} is the actual limit')

    if excluded_app_ids:
        apps = [app for app in apps if app.steam_appid not in excluded_app_ids]

    if amount > len(apps):
        raise HTTPException(
            status_code=400, detail=f'Could not obtain {amount} random apps without repeats. Try with {len(apps)}'
        )

    return random.sample(population=apps, k=amount)


def get_top100_in_2weeks_random_apps_detailed(amount: int) -> List[schemas.AppDetailed]:
    apps = []

    while (diff := amount - sum(1 for app in apps if app is not None)) > 0:
        excluded_app_ids = {app.steam_appid for app in apps if app is not None}
        random_apps = get_top100_in_2weeks_random_apps(amount=diff, excluded_app_ids=excluded_app_ids)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_detailed_app, app) for app in random_apps if app]

            for future in as_completed(futures):
                apps.append(future.result())

    apps = list(filter(None, apps))
    assert len(apps) == amount
    return apps


def get_base_app(app_id: int, index: Optional[int] = None) -> Optional[schemas.AppBase]:
    result = get_request(url=URL_STEAMSPY, params={'request': 'appdetails', 'appid': app_id})
    if not result['name']:
        return None

    return create_app_base_object(app=result, index=index)


def get_detailed_app(app_base: schemas.AppBase) -> Optional[schemas.AppDetailed]:
    # pylint: disable=too-many-locals

    app_id = app_base.steam_appid
    result = get_request(url=URL_STEAM_POWERED_APP_DETAILS, params={'appids': app_id, 'l': 'english'})[str(app_id)]
    if not result['success']:
        log.warning(f'Error while getting: {app_id} Data: {result}')
        return None

    app = result['data']
    app_type = app.get('type', None)
    short_description = app.get('short_description', None)
    detailed_description = app.get('detailed_description', None)

    screenshots_raw = app.get('screenshots', [])
    screenshots = []
    for screenshot in screenshots_raw:
        if path := screenshot.get('path_thumbnail', None):
            screenshots.append(path)

    release_date_raw = app.get('release_date', None)
    release_date = None
    if date := release_date_raw.get('date', None):
        try:
            release_date = utils.parse_date(date=date)
        except Exception as error:
            log.error(date)
            raise error

    base = dict(app_base)
    base['app_type'] = app_type
    base['screenshots'] = screenshots
    base['short_description'] = short_description
    base['detailed_description'] = detailed_description
    base['release_date'] = release_date

    return schemas.AppDetailed(**base)


def get_apps_by_title(title: str) -> List[schemas.AppBase]:
    result = get_request(f'{URL_SEARCH_APPS}/{title}')

    app_ids = [container['appid'] for container in result if 'appid' in container]

    with ThreadPoolExecutor() as executor:
        apps = executor.map(get_base_app, *(app_ids, tuple(range(len(app_ids)))))

    return list(filter(None, apps))
