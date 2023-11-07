import os
import json
import datetime
import xlsxwriter
from typing import List

from classes.Task import Task
from classes.TaskComparison import TaskComparison
from services.LiquidPlanner import fetch_tasks_by_package, fetch_tasks_by_ids, build_tasks
from utils.Utils import get_sharepoint_directory
from utils.Constants import SNAPSHOT_FILENAME_FORMAT

SPRINT_NUMBER = 22
SPRINT_PACKAGE_ID = 70546945

USER_IDS = [
    916262,   # Ollie
    1062224,  # Finn
    1071107   # Nathan
]

TASK_CRUMB_SEPARATOR = '00000'

# CSV filename example: 230101 1200 Sprint 21 Work Summary.xlsx
EXCEL_FILENAME_DATE_FORMAT = '%y%m%d %H%M'
EXCEL_FILENAME_FORMAT = '{0} Sprint {1} Work Summary.xlsx'
EXCEL_HEADER = ['Name', 'Estimated', 'Total', 'Overtime %', 'Complete %', '', 'Total Start', 'Total End', 'Logged Start', 'Logged End', 'Remaining Start', 'Remaining End']
EXCEL_CRUMB_SPACING = ' ' * 16

def group_tasks_by_tree(tasks_comparisons: List[TaskComparison]) -> dict[str, List[TaskComparison]]:
    grouped_tasks: dict[str, List[TaskComparison]] = dict()
    for task in tasks_comparisons:
        key = TASK_CRUMB_SEPARATOR.join(task.get_parent_crumbs())
        if key in grouped_tasks:
            grouped_tasks[key].append(task)
        else:
            grouped_tasks[key] = [task]

    ordered_keys = list(grouped_tasks.keys())
    ordered_keys.sort()
    return { key: grouped_tasks[key] for key in ordered_keys }

def main():
    # Read sprint start snapshot
    sprint_folder = get_sharepoint_directory(SPRINT_NUMBER)

    filename = SNAPSHOT_FILENAME_FORMAT.format(SPRINT_NUMBER)
    snapshot_file_path = os.path.join(sprint_folder, filename)
    with open(snapshot_file_path, 'r') as file:
        sprint_start_tasks_json = json.load(file)
    
    sprint_start_tasks: List[Task] = build_tasks(sprint_start_tasks_json, USER_IDS)
    sprint_start_task_ids = [task.id for task in sprint_start_tasks]

    # Get current sprint tasks
    sprint_current_tasks_json = fetch_tasks_by_package(SPRINT_PACKAGE_ID)
    sprint_current_tasks = build_tasks(sprint_current_tasks_json, USER_IDS)
    sprint_current_task_ids = [task.id for task in sprint_current_tasks]

    # Get tasks which were in start of sprint but are not in current sprint folder
    sprint_removed_task_ids = list(set(sprint_start_task_ids) - set(sprint_current_task_ids))
    sprint_removed_tasks_json = fetch_tasks_by_ids(sprint_removed_task_ids)
    sprint_removed_tasks = build_tasks(sprint_removed_tasks_json, USER_IDS)

    # Combine current sprint tasks with missing tasks
    sprint_end_tasks = sprint_current_tasks + sprint_removed_tasks

    # Create TaskComparison objects
    start_task_comparisons: TaskComparison = []
    for start_task in sprint_start_tasks:
        matching_end_tasks = [task for task in sprint_end_tasks if task.id == start_task.id]
        end_task = matching_end_tasks[0] if len(matching_end_tasks) > 0 else None
        
        if end_task is not None:
            start_task_comparisons.append(TaskComparison(start_task, end_task))
        else:
            print(f'Warning: Could not find matching end task for task: {start_task.name}')
    
    grouped_sprint_tasks = group_tasks_by_tree(start_task_comparisons)

    # Write tasks to spreadsheet
    now = datetime.datetime.now()
    file_date = now.strftime(EXCEL_FILENAME_DATE_FORMAT)
    filename = EXCEL_FILENAME_FORMAT.format(file_date, SPRINT_NUMBER)
    summary_file_path = os.path.join(sprint_folder, filename)

    workbook = xlsxwriter.Workbook(summary_file_path)
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

    row_i = write_excel_task_group(grouped_sprint_tasks, sheet, formats, row_i, first_col_i, first_task_col_i)

    # Close workbook
    closed_successfully = False
    while not closed_successfully:
        try:
            workbook.close()
            closed_successfully = True
        except xlsxwriter.exceptions.FileCreateError:
            input('Please ensure any existing versions of the Excel file are closed. Press \'Enter\' to retry.')

def write_excel_task_group(grouped_tasks: dict[str, List[TaskComparison]], sheet, formats: dict, row_i: int, first_col_i: int, first_task_col_i: int) -> int:
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

def write_excel_folder_summary(tasks: List[TaskComparison], sheet, formats: dict, row_i: int, first_col_i: int):
    sprint_start_logged = sum([task.get_start_logged() for task in tasks])
    sprint_start_remaining = sum([task.get_start_remaining() for task in tasks])
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

def write_excel_task(task: TaskComparison, sheet, formats: dict, row_i: int, first_col_i: int):
    sprint_start_logged = task.get_start_logged()
    sprint_start_remaining = task.get_start_remaining()
    sprint_end_logged = task.get_current_logged()
    sprint_end_remaining = task.get_current_remaining()

    total_end = sprint_end_logged + sprint_end_remaining
    total = total_end - sprint_start_logged

    percentage_format = formats['percentage']

    sheet.write_string(row_i, first_col_i, task.get_name())

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

if __name__ == '__main__':
    main()
