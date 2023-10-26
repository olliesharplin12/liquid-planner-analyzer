class Assignment:

    def __init__(self, id: int, task_id: int, user_id: int, logged: float, remaining_low: float, remaining_high: float):
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.logged = logged
        self.remaining_low = remaining_low
        self.remaining_high = remaining_high
    
    def get_remaining(self) -> float:
        return (self.remaining_low + self.remaining_high) / 2.0
