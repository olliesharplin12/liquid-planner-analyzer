from typing import List

from ..classes.Task import Task
from ..utils.Utils import fetch


FETCH_TIMESHEET_ENTRIES_URL = 'timesheet_entries'
FETCH_SPRINT_TASKS_URL = ''  # TODO

def fetch_tasks_by_filters(start: str, end: str, user_ids: List[str] = None) -> List[Task]:
    query_params: List[tuple[str, str]] = [('start_date', start), ('end_date', end)]
    
    response = fetch(FETCH_TIMESHEET_ENTRIES_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')
    
    # TODO: Evaluate response JSON and formulate into tasks.

    timesheet_entires = 

    tasks = [Task() for task in response.json()]

    # Filter tasks by user ids
    if user_ids is type(List) and len(user_ids) > 0:
        query_params.append(('users', ','.join(user_ids)))  # TODO

    return tasks

def fetch_tasks_at_sprint_date(sprint: int, date: str) -> List[Task]:
    query_params: List[tuple[str, str]] = [('sprint', f'Sprint {sprint}'), ('date', date)]

    response = fetch(FETCH_SPRINT_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')
    
    # TODO: Evaluate response JSON and formulate into tasks.
    
    tasks = [Task() for task in response.json()]
    return tasks
