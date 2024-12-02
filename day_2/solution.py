# Advent of Code 2024: Day 2 - Red-Nosed Reports

# Problem Context:
# The task is to analyze reactor data to determine if reports are "safe." A report is deemed safe if:
# - Levels are either all increasing or all decreasing.
# - Differences between adjacent levels are within the range of 1 to 3.
# Additionally, a "Problem Dampener" allows a single bad level to be ignored for determining safety.

# Function to read input data from a file.
def read_input(file_path):
    """
    Reads the input file and returns a list of strings, each representing a line from the file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list[str]: A list of lines from the input file.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to determine if a report is safe without modifications.
def is_safe(report):
    """
    Checks if a report is safe based on the rules:
    - Levels must be either all increasing or all decreasing.
    - Differences between adjacent levels must be within the range [-3, -2, -1, 1, 2, 3].

    Args:
        report (list[int]): A list of levels in the report.

    Returns:
        bool: True if the report is safe, False otherwise.
    """
    # Check if levels are ordered (all increasing or all decreasing).
    is_ordered = (
        all(report[i] < report[i + 1] for i in range(len(report) - 1)) or
        all(report[i] > report[i + 1] for i in range(len(report) - 1))
    )

    # Check if differences between adjacent levels are within the allowed range.
    is_delta_correct = all(
        abs(report[i + 1] - report[i]) in [1, 2, 3] for i in range(len(report) - 1)
    )

    return is_ordered and is_delta_correct

# Function to determine if a report is safe with one level ignored.
def is_safe_modified(report, tolerance_count=0):
    """
    Checks if a report can be made safe by ignoring at most one level.

    Args:
        report (list[int]): A list of levels in the report.
        tolerance_count (int): The current count of ignored levels (default is 0).

    Returns:
        bool: True if the report is safe with up to one level ignored, False otherwise.
    """
    # Terminate recursion if more than one level is ignored.
    if tolerance_count > 1:
        return False

    # Check if the report is safe as is.
    if is_safe(report):
        return True

    # Try removing each level and check if the resulting report is safe.
    for i in range(len(report)):
        new_report = report[:i] + report[i+1:]  # Remove the i-th level.
        if is_safe_modified(new_report, tolerance_count + 1):
            return True

    return False

if __name__ == '__main__':
    # Read the input data from the file.
    reports = read_input('day_2/input.txt')

    # Parse each line into a list of integers.
    reports = [list(map(int, report.split())) for report in reports]

    # Part 1: Count the number of safe reports without modifications.
    safe_report_count = sum(1 for report in reports if is_safe(report))
    print("Part 1: Number of safe reports:", safe_report_count)

    # Part 2: Count the number of safe reports allowing for one level to be ignored.
    safe_report_count_modified = sum(1 for report in reports if is_safe_modified(report))
    print("Part 2: Number of safe reports with modifications:", safe_report_count_modified)