from collections import defaultdict, deque

def parse_input(input_text):
    """
    Parses the raw puzzle input into ordering rules and updates.

    Args:
    input_text (str): The raw puzzle input as a string.

    Returns:
    tuple: A list of rules and a list of updates.
    """
    sections = input_text.strip().split("\n\n")
    rules = [tuple(map(int, line.split("|"))) for line in sections[0].split("\n")]
    updates = [list(map(int, update.split(","))) for update in sections[1].split("\n")]
    return rules, updates

def is_update_valid(update, rules):
    """
    Checks if an update follows the given ordering rules.

    Args:
    update (list): A list of page numbers in the update.
    rules (list): A list of rules as tuples (X, Y).

    Returns:
    bool: True if the update follows all ordering rules, otherwise False.
    """
    for x, y in rules:
        if x in update and y in update:
            # Ensure x appears before y in the update
            if update.index(x) > update.index(y):
                return False
    return True

def find_middle_page(update):
    """
    Finds the middle page number of a given update.

    Args:
    update (list): A list of page numbers.

    Returns:
    int: The middle page number.
    """
    n = len(update)
    return update[n // 2]

def process_part_one(input_text):
    """
    Processes the puzzle to find the sum of middle pages from valid updates.

    Args:
    input_text (str): The raw puzzle input as a string.

    Returns:
    int: The sum of middle pages from valid updates.
    """
    # Parse input
    rules, updates = parse_input(input_text)

    # Initialize the sum of middle pages
    middle_page_sum = 0

    for update in updates:
        if is_update_valid(update, rules):  # Check if update is valid
            middle_page_sum += find_middle_page(update)  # Add middle page

    return middle_page_sum

def reorder_update(update, rules):
    """
    Reorders an incorrectly-ordered update based on the given rules.

    Args:
    update (list): A list of page numbers in the update.
    rules (list): A list of rules as tuples (X, Y).

    Returns:
    list: The correctly-ordered update.
    """
    # Build a directed graph and in-degree map for topological sorting
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Consider only rules relevant to this update
    update_set = set(update)
    for x, y in rules:
        if x in update_set and y in update_set:
            graph[x].append(y)
            in_degree[y] += 1
            in_degree[x] += 0  # Ensure x is in the in-degree map

    # Perform topological sort using Kahn's algorithm
    # Read more: https://en.wikipedia.org/wiki/Topological_sorting#Algorithms
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_update = []

    while queue:
        current = queue.popleft()
        sorted_update.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

def process_part_two(input_text):
    """
    Processes the puzzle to find the sum of middle pages from fixed updates.

    Args:
    input_text (str): The raw puzzle input as a string.

    Returns:
    int: The sum of middle pages from fixed updates.
    """
    # Parse input
    rules, updates = parse_input(input_text)

    # Initialize the sum of middle pages
    middle_page_sum = 0

    for update in updates:
        if not is_update_valid(update, rules):  # Identify invalid updates
            corrected_update = reorder_update(update, rules)  # Reorder it
            middle_page_sum += find_middle_page(corrected_update)  # Add middle page
    
    return middle_page_sum

def main():
    """
    Main function to handle file input and execute the puzzle logic for both parts.
    """
    # Read input from file
    try:
        with open("day_5/input.txt", "r") as file:
            input_text = file.read()
    except FileNotFoundError:
        print("Error: input.txt not found. Please ensure the file is in the same directory as this script.")
        return

    # Process Part 1 and print the result
    part_one_result = process_part_one(input_text)
    print(f"Part 1: Sum of middle pages from valid updates: {part_one_result}")

    # Process Part 2 and print the result
    part_two_result = process_part_two(input_text)
    print(f"Part 2: Sum of middle pages from fixed updates: {part_two_result}")

def testcase():
        # Run example test case
    example_input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
    print("\n--- Example Test Case ---")
    print("Processing Part 1 for example input...")
    example_part_one_result = process_part_one(example_input)
    print(f"Part 1 Example Result (expected 137): {example_part_one_result}")

    print("Processing Part 2 for example input...")
    example_part_two_result = process_part_two(example_input)
    print(f"Part 2 Example Result (expected 123): {example_part_two_result}")
    print("--- End of Example Test Case ---\n")

# Entry point for the script
if __name__ == "__main__":
    testcase()
    main()
