from typing import List

from classes.TimesheetEntry import TimesheetEntry
from services.LiquidPlanner import fetch_timesheet_enties_by_filters, fetch_tasks_by_package, fetch_tasks_by_ids, fetch_task_snapshots
from utils.Utils import print_with_progress

SPRINT_PACKAGE_ID = 70450154
START = '2023-10-20T06:15:00+00:00'  # Must be a time equal to or just before the baseline was taken
END = '2023-10-27T06:15:00+00:00'
USER_IDS = [
    916262,   # Ollie
    1062224,  # Finn
    1071107   # Nathan
]

PRINT_FETCH_SPRINT_TASKS = 'Fetching sprint tasks...'
PRINT_FETCH_TIMESHEET_ENTRIES = 'Fetching timesheet entries...'
PRINT_FETCH_MISSING_TASKS = 'Fetching progressed tasks not in sprint package...'
PRINT_FETCH_SNAPSHOTS = 'Fetching task snapshots...'

def main():

    # Get sprint tasks and timesheet entries
    # print('Fetching sprint tasks... 100%')
    print_with_progress(PRINT_FETCH_SPRINT_TASKS, 0, 1, False)
    sprint_tasks = fetch_tasks_by_package(SPRINT_PACKAGE_ID)
    print_with_progress(PRINT_FETCH_SPRINT_TASKS, 1, 1, False)

    print_with_progress(PRINT_FETCH_TIMESHEET_ENTRIES, 0, len(USER_IDS), True)
    timesheet_entries: List[TimesheetEntry] = []
    for i in range(len(USER_IDS)):
        user_id = USER_IDS[i]
        timesheet_entries += fetch_timesheet_enties_by_filters(START, END, user_id)
        print_with_progress(PRINT_FETCH_TIMESHEET_ENTRIES, (i + 1), len(USER_IDS), False)
    
    # Fetch tasks which are not in sprint package which have been worked on within the time range
    # print('\nFetching progressed tasks not in sprint package... 100%')
    print_with_progress(PRINT_FETCH_MISSING_TASKS, 0, 1, True)
    sprint_task_ids = [task.id for task in sprint_tasks]
    timesheet_entry_task_ids = set([entry.task_id for entry in timesheet_entries])

    missing_task_ids = [task_id for task_id in timesheet_entry_task_ids if task_id not in sprint_task_ids]
    if len(missing_task_ids) > 0:
        sprint_tasks += fetch_tasks_by_ids(missing_task_ids)
    print_with_progress(PRINT_FETCH_MISSING_TASKS, 1, 1, False)

    # Get task snapshots (history) and set sprint start snapshot
    print_with_progress(PRINT_FETCH_SNAPSHOTS, 0, len(sprint_tasks), True)
    for i in range(len(sprint_tasks)):
        task = sprint_tasks[i]
        snapshots = fetch_task_snapshots(task.id)
        task.set_sprint_start_snapshot(START, END, snapshots)

        print_with_progress(PRINT_FETCH_SNAPSHOTS, (i + 1), len(sprint_tasks), False)

    # Assign timesheet entries to tasks
    for task in sprint_tasks:
        if task.id in timesheet_entry_task_ids:
            task.set_timesheet_entries([entry for entry in timesheet_entries if entry.task_id == task.id])
        else:
            task.set_timesheet_entries([])

    # Write tasks to spreadsheet
    # TODO

    print()
    for task in sprint_tasks:
        print(task)

if __name__ == "__main__":
    main()
