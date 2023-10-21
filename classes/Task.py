from typing import List
from classes.Activity import Activity

class Task:

    def __init__(self, id, name, activities: List[Activity]):
        self.id: str = id
        self.name: str = name
        self.activities: List[Activity] = activities
    
    def get_logged_by_users(self, user_ids: List[str] = None) -> float:
        return sum([activity.logged for activity in self.activities if user_ids is None or activity.user_id in user_ids])
    
    def get_remaining_by_users(self, user_ids: List[str] = None) -> float:
        return sum([activity.remaining for activity in self.activities if user_ids is None or activity.user_id in user_ids])
    
    def get_total_by_users(self, user_ids: List[str] = None) -> float:
        return sum([activity.get_total() for activity in self.activities if user_ids is None or activity.user_id in user_ids])
