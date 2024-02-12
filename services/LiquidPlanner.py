from typing import List
from classes.Task import Task
from classes.Assignment import Assignment
from classes.TimesheetEntry import TimesheetEntry
from utils.Http import get

FETCH_TASKS_URL = 'tasks'
FETCH_TIMESHEET_ENTRIES_URL = 'timesheet_entries'

def build_assignments(json: List[dict], user_ids: List[int]) -> List[Assignment]:
    return [
        Assignment(
            assignment['id'],
            assignment['treeitem_id'],
            assignment['person_id'],
            assignment['hours_logged'],
            assignment['low_effort_remaining'],
            assignment['high_effort_remaining']
        ) for assignment in json if assignment['person_id'] in user_ids
    ]

def build_tasks(json: List[dict], user_ids: List[int]) -> List[Task]:
    return [
        Task(task['id'],
            task['name'],
            task['package_id'],
            task['parent_crumbs'],
            build_assignments(task['assignments'], user_ids)
        ) for task in json]

def build_timesheet_entries(json: List[dict]) -> List[TimesheetEntry]:
    return [TimesheetEntry(entry['item_id'], entry['activity_id'], entry['member_id'], entry['work']) for entry in json]

def fetch_tasks_by_package(package_id: int) -> dict:
    query_params: List[tuple[str, str]] = [('filter[]=package_id', package_id)]

    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return response.json()

def fetch_tasks_by_ids(task_ids: List[int]) -> dict:
    query_params: List[tuple[str, str]] = [('filter[]=id', ','.join(map(str, task_ids)))]

    response = get(FETCH_TASKS_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return response.json()

def fetch_timesheet_enties_by_filters(start: str, user_id: int) -> List[TimesheetEntry]:
    query_params: List[tuple[str, str]] = [('start_date', start), ('member_id', user_id)]
    
    response = get(FETCH_TIMESHEET_ENTRIES_URL, query_params)
    if response.status_code != 200:
        raise Exception(f'Response Error: {response.text}')

    return response.json()
