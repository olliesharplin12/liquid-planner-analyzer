from typing import List, Union

from classes.Task import Task
from classes.TimesheetEntry import TimesheetEntry

class TaskComparison:

    def __init__(self, end_task: Task, start_task: Task = None, timesheet_entries: List[TimesheetEntry] = None):
        self.end_task = end_task
        self.start_task = start_task
        self.timesheet_entries = timesheet_entries
    
    def get_name(self) -> str:
        return self.end_task.name
    
    def get_parent_crumbs(self) -> List[str]:
        return self.end_task.parent_crumbs[1:]
    
    def get_start_logged(self) -> float:
        self.check_start_task_exists()
        return self.start_task.get_current_logged()

    def get_start_remaining(self) -> Union[float, None]:
        self.check_start_task_exists()
        return self.start_task.get_current_remaining()
    
    def get_start_total(self) -> Union[float, None]:
        self.check_start_task_exists()
        return self.get_start_logged() + self.get_start_remaining()
    
    def get_current_logged(self) -> float:
        return self.end_task.get_current_logged()
    
    def get_current_remaining(self) -> float:
        return self.end_task.get_current_remaining()
    
    def get_current_total(self) -> float:
        return self.get_current_logged() + self.get_current_remaining()

    def get_timesheet_entry_logged_time(self) -> float:
        self.check_timesheet_entries_exist()
        return sum([entry.logged for entry in self.timesheet_entries])

    def check_start_task_exists(self):
        if self.start_task is None:
            raise Exception('Attempted to access start task data which does not exist')

    def check_timesheet_entries_exist(self):
        if self.timesheet_entries is None:
            raise Exception('Attempted to access timesheet entries which do not exist')
