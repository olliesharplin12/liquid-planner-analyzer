from typing import List

from utils.FetchTasks import fetch_tasks_at_sprint_date, fetch_tasks_by_filters


SPRINT: int = 21
START: str = '2023-10-21'
END: str = '2023-10-28'
USER_IDS: List[str] = []

# Fetch start tasks by sprint and date, and end tasks by select users and time range.
start_tasks = fetch_tasks_at_sprint_date(SPRINT, START)  # TODO: Does this need to filter by users?
end_tasks = fetch_tasks_by_filters(START, END, USER_IDS)

# If a sprint start task does not exist in end tasks, ensure it is retrieved.
end_task_ids = [task.id for task in end_tasks]
missing_task_ids = [task.id for task in start_tasks if task.id not in end_task_ids]

end_tasks_by_sprint = fetch_tasks_at_sprint_date(SPRINT, END)  # TODO: What if the task was removed from the sprint?
missing_tasks = [task for task in end_tasks_by_sprint if task.id in missing_task_ids]

# Combine end tasks
end_tasks += missing_tasks

