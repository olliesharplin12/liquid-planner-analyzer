from typing import List
from classes.Task import Task
from classes.Assignment import Assignment
from classes.TimesheetEntry import TimesheetEntry
from classes.Snapshot import Snapshot
from utils.Http import get

FETCH_TIMESHEET_ENTRIES_URL = 'timesheet_entries'
FETCH_TASKS_URL = 'tasks'
FETCH_TREEITEM_SNAPSHOTS_URL_FORMAT = 'treeitems/{0}/snapshots'

def build_assignments(json: List[dict]) -> List[Assignment]:
    return [
        Assignment(
            assignment['id'],
            assignment['treeitem_id'],
            assignment['person_id'],
            assignment['hours_logged'],
            assignment['low_effort_remaining'],
            assignment['high_effort_remaining']
        ) for assignment in json
    ]

def build_tasks(json: List[dict]) -> List[Task]:
    return [
        Task(task['id'],
            task['name'],
            task['package_id'],
            task['parent_crumbs'],
            build_assignments(task['assignments'])
        ) for task in json]

def build_timesheet_entries(json: List[dict]) -> List[TimesheetEntry]:
    return [TimesheetEntry(entry['item_id'], entry['activity_id'], entry['member_id'], entry['work']) for entry in json]

def build_snapshots(json: List[dict]) -> List[Snapshot]:
    return [Snapshot(snapshot['id'], snapshot['created_at'], snapshot['low'], snapshot['high']) for snapshot in json]

def fetch_timesheet_enties_by_filters(start: str, end: str, user_id: int) -> List[TimesheetEntry]:
    query_params: List[tuple[str, str]] = [('start_date', start), ('end_date', end), ('member_id', user_id)]
    
    response = get(FETCH_TIMESHEET_ENTRIES_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return build_timesheet_entries(response.json())

def fetch_tasks_by_package(package_id: int) -> List[Task]:
    query_params: List[tuple[str, str]] = [('filter[]=package_id', package_id)]

    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return build_tasks(response.json())

def fetch_tasks_by_ids(task_ids: List[int]):
    query_params: List[tuple[str, str]] = [('filter[]=id', ','.join(map(str, task_ids)))]

    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return build_tasks(response.json())

def fetch_tasks_by_tags(tags: List[str]):
    query_params: List[tuple[str, str]] = [('filter[]', f'tags include {",".join(tags)}')]
    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return build_tasks(response.json())

def fetch_task_snapshots(task_id: int) -> List[Snapshot]:
    response = get(FETCH_TREEITEM_SNAPSHOTS_URL_FORMAT.format(task_id))
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return build_snapshots(response.json())

def fetch_tasks_by_package_as_json(package_id: int) -> dict:
    query_params: List[tuple[str, str]] = [('filter[]=package_id', package_id)]

    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return response.json()
