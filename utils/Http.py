import requests
from requests.auth import HTTPBasicAuth

from env import LIQUID_PLANNER_EMAIL, LIQUID_PLANNER_PASSWORD
from requests import Response
from typing import List, Union

WORKSPACE_ID = 164559
BASE_URL = f'https://app.liquidplanner.com/api/v1/workspaces/{WORKSPACE_ID}/'
AUTH = HTTPBasicAuth(LIQUID_PLANNER_EMAIL, LIQUID_PLANNER_PASSWORD)

def build_url(url_suffix: str, query_params: Union[List[tuple[str, str]], None] = None) -> str:
    if query_params is not None and len(query_params) > 0:
        # TODO: Convert to url encoded string?
        return BASE_URL + url_suffix + '?' + '&'.join([f'{key}={value}' for key, value in query_params])
    else:
        return BASE_URL + url_suffix

def get(url_suffix: str, query_params: Union[List[tuple[str, str]], None] = None) -> Response:
    url = build_url(url_suffix, query_params)
    return requests.get(url, auth=AUTH)

def post(url_suffix: str, body: dict) -> Response:
    url = build_url(url_suffix)
    return requests.post(url, data=body, auth=AUTH)

def delete(url_suffix: str) -> Response:
    url = build_url(url_suffix)
    return requests.delete(url, auth=AUTH)
