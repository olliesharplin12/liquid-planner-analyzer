import datetime
import xlsxwriter
from typing import List


from classes.TimesheetEntry import TimesheetEntry
from classes.Task import Task
from services.LiquidPlanner import fetch_timesheet_enties_by_filters, fetch_tasks_by_package, fetch_tasks_by_ids, fetch_task_snapshots, fetch_tasks_by_tags
from utils.Utils import print_with_progress

SPRINT_NUMBER = 21
SPRINT_PACKAGE_ID = 70450154
SPRINT_TASKS_TAG = 'SprintPlanned'
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
PRINT_FETCH_SPRINT_START_TASKS = 'Fetching tasks in sprint at beginning of sprint...'
PRINT_FETCH_SNAPSHOTS = 'Fetching task snapshots...'

TASK_CRUMB_SEPARATOR = '00000'

# CSV filename example: 230101 1200 Sprint 21 Work Summary.xlsx
EXCEL_FILENAME_DATE_FORMAT = '%y%m%d %H%M'
EXCEL_FILENAME_FORMAT = '{0} Sprint {1} Work Summary.xlsx'
EXCEL_HEADER = ['Name', 'Estimated', 'Total', 'Overtime %', 'Complete %', '', 'Total Start', 'Total End', 'Logged Start', 'Logged End', 'Remaining Start', 'Remaining End']
EXCEL_CRUMB_SPACING = ' ' * 16

def write_excel_task_group(grouped_tasks: dict[str, List[Task]], sheet, formats: dict, row_i: int, first_col_i: int, first_task_col_i: int) -> int:
    previous_crumb = []
    for key, tasks in grouped_tasks.items():
        col_i = first_col_i
        crumbs = key.split(TASK_CRUMB_SEPARATOR)

        for i in range(len(crumbs)):
            crumb = crumbs[i]
            if len(previous_crumb) <= i:
                previous_crumb.append(None)
            
            if crumb != previous_crumb[i]:
                sheet.write(row_i, col_i, (EXCEL_CRUMB_SPACING * i) + crumb)
                previous_crumb[i] = crumb
                previous_crumb = previous_crumb[:i+1]
                row_i += 1
        
        if len(tasks) > 1:
            write_excel_folder_summary(tasks, sheet, formats, row_i - 1, first_task_col_i)

        for task in tasks:
            write_excel_task(task, sheet, formats, row_i, first_task_col_i)
            row_i += 1
        row_i += 1
    return row_i

def write_excel_folder_summary(tasks: List[Task], sheet, formats: dict, row_i: int, first_col_i: int):
    sprint_start_logged = sum([task.get_logged_before_timesheet_entries() for task in tasks])
    sprint_start_remaining = sum([0 if task.get_remaining_at_sprint_start_snapshot() is None else task.get_remaining_at_sprint_start_snapshot() for task in tasks])
    sprint_end_logged = sum([task.get_current_logged() for task in tasks])
    sprint_end_remaining = sum([task.get_current_remaining() for task in tasks])

    total_end = sprint_end_logged + sprint_end_remaining
    total = total_end - sprint_start_logged

    bold_format = formats['bold']
    bold_percentage_format = formats['bold_percentage']

    sheet.write_number(row_i, first_col_i+1, sprint_start_remaining, bold_format)
    sheet.write_number(row_i, first_col_i+2, total_end - sprint_start_logged, bold_format)
    if sprint_start_remaining > 0 and total / sprint_start_remaining > 1:
        sheet.write_number(row_i, first_col_i+3, total / sprint_start_remaining, bold_percentage_format)
    if total_end - sprint_start_logged > 0:
        sheet.write_number(row_i, first_col_i+4, (sprint_end_logged - sprint_start_logged) / total, bold_percentage_format)

    sheet.write_number(row_i, first_col_i+6, sprint_start_logged + sprint_start_remaining, bold_format)
    sheet.write_number(row_i, first_col_i+7, sprint_end_logged + sprint_end_remaining, bold_format)

    sheet.write_number(row_i, first_col_i+8, sprint_start_logged, bold_format)
    sheet.write_number(row_i, first_col_i+9, sprint_end_logged, bold_format)

    sheet.write_number(row_i, first_col_i+10, sprint_start_remaining, bold_format)
    sheet.write_number(row_i, first_col_i+11, sprint_end_remaining, bold_format)

def write_excel_task(task: Task, sheet, formats: dict, row_i: int, first_col_i: int):
    sprint_start_logged = task.get_logged_before_timesheet_entries()
    sprint_start_remaining = 0 if task.get_remaining_at_sprint_start_snapshot() is None else task.get_remaining_at_sprint_start_snapshot()
    sprint_end_logged = task.get_current_logged()
    sprint_end_remaining = task.get_current_remaining()

    total_end = sprint_end_logged + sprint_end_remaining
    total = total_end - sprint_start_logged

    percentage_format = formats['percentage']

    sheet.write_string(row_i, first_col_i, task.name)

    sheet.write_number(row_i, first_col_i+1, sprint_start_remaining)
    sheet.write_number(row_i, first_col_i+2, total_end - sprint_start_logged)
    if sprint_start_remaining > 0 and total / sprint_start_remaining > 1:
        sheet.write_number(row_i, first_col_i+3, total / sprint_start_remaining, percentage_format)
    if total_end - sprint_start_logged > 0:
        sheet.write_number(row_i, first_col_i+4, (sprint_end_logged - sprint_start_logged) / total, percentage_format)
    
    sheet.write_number(row_i, first_col_i+6, sprint_start_logged + sprint_start_remaining)
    sheet.write_number(row_i, first_col_i+7, sprint_end_logged + sprint_end_remaining)

    sheet.write_number(row_i, first_col_i+8, sprint_start_logged)
    sheet.write_number(row_i, first_col_i+9, sprint_end_logged)

    sheet.write_number(row_i, first_col_i+10, sprint_start_remaining)
    sheet.write_number(row_i, first_col_i+11, sprint_end_remaining)

def group_tasks_by_tree(tasks: List[Task]) -> dict[str, List[Task]]:
    grouped_tasks = dict()
    for task in tasks:
        key = TASK_CRUMB_SEPARATOR.join(task.parent_crumbs[1:])
        if key in grouped_tasks:
            grouped_tasks[key].append(task)
        else:
            grouped_tasks[key] = [task]

    ordered_keys = list(grouped_tasks.keys())
    ordered_keys.sort()
    return { key: grouped_tasks[key] for key in ordered_keys }

def main():
    # Get sprint tasks and timesheet entries
    print_with_progress(PRINT_FETCH_SPRINT_TASKS, 0, 1, False)
    sprint_tasks = fetch_tasks_by_package(SPRINT_PACKAGE_ID)
    sprint_task_ids = [task.id for task in sprint_tasks]
    print_with_progress(PRINT_FETCH_SPRINT_TASKS, 1, 1, False)

    print_with_progress(PRINT_FETCH_TIMESHEET_ENTRIES, 0, len(USER_IDS), True)
    timesheet_entries: List[TimesheetEntry] = []
    for i in range(len(USER_IDS)):
        user_id = USER_IDS[i]
        timesheet_entries += fetch_timesheet_enties_by_filters(START, END, user_id)
        print_with_progress(PRINT_FETCH_TIMESHEET_ENTRIES, (i + 1), len(USER_IDS), False)
    
    # Fetch tasks which are not in sprint package which have been worked on within the time range
    print_with_progress(PRINT_FETCH_MISSING_TASKS, 0, 1, True)
    timesheet_entry_task_ids = set([entry.task_id for entry in timesheet_entries])
    missing_task_ids = [task_id for task_id in timesheet_entry_task_ids if task_id not in sprint_task_ids]
    if len(missing_task_ids) > 0:
        sprint_tasks += fetch_tasks_by_ids(missing_task_ids)
        sprint_task_ids = [task.id for task in sprint_tasks]
    print_with_progress(PRINT_FETCH_MISSING_TASKS, 1, 1, False)

    # Fetch tasks which were in the sprint package at the start of the sprint, and add to tasks if missing
    print_with_progress(PRINT_FETCH_SPRINT_START_TASKS, 0, 1, True)
    sprint_start_tagged_tasks = fetch_tasks_by_tags([SPRINT_TASKS_TAG])
    sprint_start_tagged_task_ids = [task.id for task in sprint_start_tagged_tasks]

    sprint_tasks += [task for task in sprint_start_tagged_tasks if task.id not in sprint_task_ids]
    sprint_task_ids = [task.id for task in sprint_tasks]
    print_with_progress(PRINT_FETCH_SPRINT_START_TASKS, 1, 1, False)

    # Get task snapshots (history) and set sprint start snapshot
    print_with_progress(PRINT_FETCH_SNAPSHOTS, 0, len(sprint_tasks), True)
    for i in range(len(sprint_tasks)):
        task = sprint_tasks[i]
        snapshots = fetch_task_snapshots(task.id)
        task.set_sprint_start_snapshot(START, END, snapshots)

        print_with_progress(PRINT_FETCH_SNAPSHOTS, (i + 1), len(sprint_tasks), False)
    print()

    # Assign timesheet entries to tasks
    for task in sprint_tasks:
        if task.id in timesheet_entry_task_ids:
            task.set_timesheet_entries([entry for entry in timesheet_entries if entry.task_id == task.id])
        else:
            task.set_timesheet_entries([])
    
    # Identify tasks which existing in the sprint at the start and the ones which have been unexpectedly worked on
    sprint_start_tasks: List[Task] = []
    non_sprint_start_tasks: List[Task] = []
    for task in sprint_tasks:
        if task.id in sprint_start_tagged_task_ids:
            sprint_start_tasks.append(task)
        else:
            non_sprint_start_tasks.append(task)
    
    grouped_sprint_start_tasks_dict = group_tasks_by_tree(sprint_start_tasks)
    grouped_non_sprint_start_tasks_dict = group_tasks_by_tree(non_sprint_start_tasks)

    # Write tasks to spreadsheet
    now = datetime.datetime.now()
    file_date = now.strftime(EXCEL_FILENAME_DATE_FORMAT)
    filename = EXCEL_FILENAME_FORMAT.format(file_date, SPRINT_NUMBER)

    workbook = xlsxwriter.Workbook(filename)
    sheet = workbook.add_worksheet(name='Sprint {0}'.format(SPRINT_NUMBER))

    formats = dict()
    formats['bold'] = workbook.add_format({ 'bold': True })
    formats['percentage'] = workbook.add_format({ 'num_format': '0%' })
    formats['bold_percentage'] = workbook.add_format({ 'bold': True, 'num_format': '0%' })

    row_i = 0
    first_col_i = 0
    first_task_col_i = 1

    # Write header
    for col_i in range(len(EXCEL_HEADER)):
        sheet.write(row_i, first_task_col_i + col_i, EXCEL_HEADER[col_i], formats['bold'])
    row_i += 2

    # Write tasks in sprint originally
    sheet.write(row_i, 0, 'Original Sprint Tasks', formats['bold'])
    row_i += 2

    row_i = write_excel_task_group(grouped_sprint_start_tasks_dict, sheet, formats, row_i, first_col_i, first_task_col_i)
    
    # Write tasks added to sprint after start
    sheet.write(row_i, 0, 'Tasks Added to Sprint', formats['bold'])
    row_i += 2

    row_i = write_excel_task_group(grouped_non_sprint_start_tasks_dict, sheet, formats, row_i, first_col_i, first_task_col_i)

    # Close workbook
    closed_successfully = False
    while not closed_successfully:
        try:
            workbook.close()
            closed_successfully = True
        except xlsxwriter.exceptions.FileCreateError:
            input('Please ensure any existing versions of the Excel file are closed. Press \'Enter\' to retry.')

if __name__ == "__main__":
    main()
