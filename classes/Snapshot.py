class Snapshot:

    def __init__(self, task_id: str, created_at: str, low_remaining: float, high_remaining: float):
        self.task_id = task_id
        self.created_at = created_at
        self.low_remaining = low_remaining
        self.high_remaining = high_remaining
    
    def get_remaining(self) -> float:
        return (self.low_remaining + self.high_remaining) / 2.0
