import logging
import time
import urllib.parse
from typing import Optional

import requests
from requests.exceptions import SSLError

from steam_deals.core.exception import HTTPException

log = logging.getLogger('steam_deals')


def get_request(url: str, params: Optional[dict] = None, attempts: int = 3) -> dict:
    """Return json-formatted response of a get request using optional parameters."""

    if attempts <= 0:
        raise HTTPException(status_code=503, detail='External service is unavailable. Please try again later.')

    try:
        log.debug(f'Trying to get URL: {create_url_with_params(url=url, params=params)}')
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
