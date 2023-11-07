import sys
import os

from utils.Constants import SHAREPOINT_DIRECTORY, SPRINT_FOLDER_FORMAT

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

def get_sharepoint_directory(sprint_number: int) -> str:
    user_directory = os.path.expanduser('~')
    sharepoint_folder = os.path.join(user_directory, SHAREPOINT_DIRECTORY)
    if not os.path.isdir(sharepoint_folder):
        raise Exception('Please ensure the Admin SharePoint directory is synced to your computer')
    
    sprint_folder = os.path.join(sharepoint_folder, SPRINT_FOLDER_FORMAT.format(sprint_number))
    if not os.path.isdir(sprint_folder):
        os.mkdir(sprint_folder)
    
    return sprint_folder
