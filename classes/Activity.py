class Activity:

    def __init__(self, id: str, user_id: str, logged: float, remaining: float):
        self.id = id
        self.user_id = user_id
        self.logged = logged
        self.remaining = remaining
    
    def get_total(self):
        return self.logged + self.remaining
  