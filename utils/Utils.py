import requests
import sys
from requests.auth import HTTPBasicAuth

from env import LIQUID_PLANNER_EMAIL, LIQUID_PLANNER_PASSWORD
from requests import Response
from typing import List

WORKSPACE_ID = 164559
BASE_URL = f'https://app.liquidplanner.com/api/v1/workspaces/{WORKSPACE_ID}/'
AUTH = HTTPBasicAuth(LIQUID_PLANNER_EMAIL, LIQUID_PLANNER_PASSWORD)

def build_url(url_suffix: str, query_params: List[tuple[str, str]] | None) -> str:
    if query_params is not None and len(query_params) > 0:
        # TODO: Convert to url encoded string?
        return BASE_URL + url_suffix + '?' + '&'.join([f'{key}={value}' for key, value in query_params])
    else:
        return BASE_URL + url_suffix

def fetch(url_suffix, query_params: List[tuple[str, str]] | None = None) -> Response:
    url = build_url(url_suffix, query_params)
    return requests.get(url, auth=AUTH)

def print_with_progress(prefix: str, current: float, total: float, force_new: bool, dp: int = 0) -> str:
    if force_new:
        print()
    sys.stdout.write(f'\r{prefix} {format_percentage(current, total, dp)}')
    sys.stdout.flush()

def format_percentage(current: float, total: float, dp: int = 0) -> str:
    percentage = 100.0 * current / total
    if dp <= 0:
        return f'{str(round(percentage)).rjust(3)}%'
    else:
        return f'{str(round(percentage, dp)).rjust(4 + dp)}%'
