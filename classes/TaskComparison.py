from typing import List

from classes.Task import Task

class TaskComparison:

    def __init__(self, start_task: Task, end_task: Task):
        self.start_task = start_task
        self.end_task = end_task
    
    def get_name(self) -> str:
        return self.end_task.name
    
    def get_parent_crumbs(self) -> List[str]:
        return self.end_task.parent_crumbs[1:]
    
    def get_start_logged(self) -> float | None:
        return self.start_task.get_current_logged()

    def get_start_remaining(self) -> float | None:
        return self.start_task.get_current_remaining()
    
    def get_start_total(self) -> float | None:
        return self.get_start_logged() + self.get_start_remaining()
    
    def get_current_logged(self) -> float:
        return self.end_task.get_current_logged()
    
    def get_current_remaining(self) -> float:
        return self.end_task.get_current_remaining()
    
    def get_current_total(self) -> float:
        return self.get_current_logged() + self.get_current_remaining()
