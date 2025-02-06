class TimesheetEntry():

    def __init__(self, task_id: int, activity_id: int, member_id: int, logged: float):
        self.task_id = task_id
        self.activity_id = activity_id
        self.member_id = member_id
        self.logged = logged
