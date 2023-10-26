from typing import List
from classes.Assignment import Assignment
from classes.TimesheetEntry import TimesheetEntry
from classes.Snapshot import Snapshot

class Task:

    def __init__(self, id: int, name: str, package_id: int, assignments: List[Assignment]):
        self.id = id
        self.name = name
        self.package_id = package_id
        self.assignments = assignments
        self.timesheet_entries: List[TimesheetEntry] = None
        self.sprint_start_snapshot: Snapshot | None = None
    
    def set_timesheet_entries(self, timesheet_entries: List[TimesheetEntry]):
        self.timesheet_entries = timesheet_entries
    
    def set_sprint_start_snapshot(self, start: str, end: str, snapshots: List[Snapshot]):
        snapshots_in_sprint = [
            snapshot for snapshot in snapshots if snapshot.created_at >= start and snapshot.created_at <= end
        ]

        if len(snapshots_in_sprint) > 0:
            self.sprint_start_snapshot = sorted(snapshots_in_sprint, key=lambda x: x.created_at)[0]
    
    def get_current_logged(self) -> float:
        return sum([assignment.logged for assignment in self.assignments])
    
    def get_current_remaining(self) -> float:
        return sum([assignment.get_remaining() for assignment in self.assignments])
    
    def get_current_total(self) -> float:
        return self.get_logged() + self.get_remaining()

    def get_logged_before_timesheet_entries(self) -> float:
        logged_in_timesheets = sum([entry.logged for entry in self.timesheet_entries])
        return self.get_current_logged() - logged_in_timesheets

    def get_remaining_at_sprint_start_snapshot(self) -> float | None:
        if self.sprint_start_snapshot is None:
            return None
        else:
            return self.sprint_start_snapshot.get_remaining()

    def __str__(self):
        return f'{self.name}, {self.get_logged_before_timesheet_entries()}, {self.get_remaining_at_sprint_start_snapshot()}, {self.get_current_logged()}, {self.get_current_remaining()}'
