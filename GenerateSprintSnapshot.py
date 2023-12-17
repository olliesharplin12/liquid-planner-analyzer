import json
import os

from utils.Constants import SNAPSHOT_FILENAME_FORMAT
from utils.Utils import get_sharepoint_directory
from services.LiquidPlanner import fetch_tasks_by_package

SPRINT_NUMBER = 22
SPRINT_PACKAGE_ID = 70546945

def main():
    sharepoint_folder = get_sharepoint_directory(SPRINT_NUMBER)
    filename = SNAPSHOT_FILENAME_FORMAT.format(SPRINT_NUMBER)
    file_path = os.path.join(sharepoint_folder, filename)

    if os.path.isfile(file_path):
        print('A sprint {0} start snapshot already exists. Do you want to overwrite? (y/n)'.format(SPRINT_NUMBER))
        if input().lower() != 'y':
            print('Cancelled')
            return

    sprint_tasks = fetch_tasks_by_package(SPRINT_PACKAGE_ID)

    with open(file_path, 'w') as file:
        json.dump(sprint_tasks, file, indent=4)

    print('Created sprint snapshot successfully')

if __name__ == '__main__':
    main()
