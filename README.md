# Setup Development Environment

- IDE: VS Code
- Install Python v3.10+ (ensure added to path)
- Python Package Install Command: `pip install xlsxwriter requests`


# Sprint Overtime Work Analyser

Fetches all tasks for selected users and a time range. Uses a baseline view (or similar aspect) to compare tasks time at end of time range against baseline view. Seperates tasks out which were added after the start time. Creates a spreadsheet from the data.

### Requires
- Fetch all tasks/activities, filtering by selected users and time range.
- Identify logged and remaining times at start of period.
- Identify logged and remaining times at end of period.
- Filter tasks which were created after the start time.
- Create thresholds for which tasks are considered overtime and filter them.
- Create Excel spreadsheet based on data.

### API Capabilities
- Can fetch tasks containing:
    - Name
    - Remaining time
    - Logged time
- Can fetch task snapshot containing:
    - Remaining time
- Can fetch timesheet entries containing:
    - Logged time

### Get Sprint Start Data
- Get tasks in Sprint (by package and timesheet entries within date range).
- Get logged time by current logged time - timesheet entries in date range.
- Get remaining time using snapshot.

### Get Sprint End Data
- Get tasks (all info is contained).

### TODO
- Include timesheets from unspecified users when generating start logged time.
- Add visual element for task being done in Excel output.
- Update README documentation about script.


# Personal Work Split Analyser

Grabs all tasks for a single user within a time range and creates a spreadsheet summary of how much time was spent against each tasks tag.

### Requires
- Fetch all tasks/activities, filtering by single user and time range.
- Seperates tasks by tag.
- Logs time per tag.
