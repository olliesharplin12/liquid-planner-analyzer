from typing import List
from classes.Assignment import Assignment

class Task:

    def __init__(self, id: int, name: str, package_id: int, parent_crumbs: List[str], assignments: List[Assignment]):
        self.id = id
        self.name = name
        self.package_id = package_id
        self.parent_crumbs = parent_crumbs
        self.assignments = assignments
    
    def get_current_logged(self) -> float:
        return sum([assignment.logged for assignment in self.assignments])
    
    def get_current_remaining(self) -> float:
        return sum([assignment.get_remaining() for assignment in self.assignments])
    
    def get_current_total(self) -> float:
        return self.get_current_logged() + self.get_current_remaining()
