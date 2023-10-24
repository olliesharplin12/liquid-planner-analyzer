import requests
from requests import Response
from typing import List

WORKSPACE_ID = ""  # TODO
BASE_URL = 'https://app.liquidplanner.com/api/v1/workspaces/{}/'  # TODO

def build_url(url_suffix: str, query_params: List[tuple[str, str]]) -> str:
    if len(query_params) > 0:
        # TODO: Convert to url encoded string.
        return BASE_URL + url_suffix + '?' + '&'.join([f'{key}={value}' for key, value in query_params])
    else:
        return BASE_URL + url_suffix

def fetch(url_suffix, query_params: List[tuple[str, str]]) -> Response:
    url = build_url(url_suffix, query_params)
    return requests.get(url)
