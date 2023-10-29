import sys

def print_with_progress(prefix: str, current: float, total: float, force_new: bool, dp: int = 0) -> str:
    if force_new:
        print()
    sys.stdout.write(f'\r{prefix} {format_percentage(current, total, dp)}')
    sys.stdout.flush()

def format_percentage(current: float, total: float, dp: int = 0) -> str:
    percentage = 100.0 * current / total
    if dp <= 0:
        return f'{str(round(percentage)).rjust(3)}%'
    else:
        return f'{str(round(percentage, dp)).rjust(4 + dp)}%'
