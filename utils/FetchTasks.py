import requests
from typing import List

from ..classes.Task import Task
from ..utils.Utils import build_url


BASE_URL = ''    # TODO
FETCH_TASKS_URL = f'{BASE_URL}/'  # TODO
FETCH_SPRINT_TASKS_URL = f'{BASE_URL}/'  # TODO

def fetch_tasks_by_filters(start: str, end: str, user_ids: List[str] = None) -> List[Task]:
    query_params: List[tuple[str, str]] = [('start', start), ('end', end)]

    if user_ids is type(List):
        query_params.append(('users', ','.join(user_ids)))  # TODO

    url = build_url(FETCH_TASKS_URL, query_params)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Response Error: {response.message}')  # TODO

    tasks = [Task() for task in response.json()]
    return tasks

def fetch_tasks_at_sprint_date(sprint: int, date: str) -> List[Task]:
    query_params: List[tuple[str, str]] = [('sprint', f'Sprint {sprint}'), ('date', date)]

    url = build_url(FETCH_SPRINT_TASKS_URL, query_params)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Response Error: {response.message}')  # TODO
    
    tasks = [Task() for task in response.json()]
    return tasks
