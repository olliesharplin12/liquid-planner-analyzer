import json
import os

from utils.Constants import SNAPSHOT_FILENAME_FORMAT
from utils.Utils import get_sharepoint_directory
from services.LiquidPlanner import fetch_tasks_by_package_as_json

SPRINT_NUMBER = 22
SPRINT_PACKAGE_ID = 70546945

def main():
    sharepoint_folder = get_sharepoint_directory(SPRINT_NUMBER)

    sprint_tasks = fetch_tasks_by_package_as_json(SPRINT_PACKAGE_ID)

    filename = SNAPSHOT_FILENAME_FORMAT.format(SPRINT_NUMBER)
    file_path = os.path.join(sharepoint_folder, filename)
    with open(file_path, 'w') as file:
        json.dump(sprint_tasks, file, indent=4)

    print('Created sprint snapshot successfully')

if __name__ == '__main__':
    main()
