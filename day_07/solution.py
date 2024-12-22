# Advent of Code 2024 - Day 7: Bridge Repair
# This Python script solves both Part 1 and Part 2 of the problem by determining
# which equations can be made valid using different operators:
# - Part 1: `+` (addition) and `*` (multiplication).
# - Part 2: Adds `||` (concatenation) to the operators.
# The input is read from a file named "input.txt".

def read_input(file_path):
    """
    Reads the input from the specified file and parses it into a list of tuples.
    Each tuple contains the target value and a list of numbers from the equation.

    Example Input:
        190: 10 19
        3267: 81 40 27

    Parsed Output:
        [(190, [10, 19]), (3267, [81, 40, 27])]

    :param file_path: Path to the input file (e.g., "input.txt").
    :return: List of tuples, where each tuple is (target_value, [numbers]).
    """
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into target value and numbers
            target, numbers = line.strip().split(':')
            target = int(target)
            numbers = list(map(int, numbers.split()))
            equations.append((target, numbers))
    return equations

def evaluate_expression(numbers, ops):
    """
    Evaluates an expression given a list of numbers and a list of operators.
    Operators are applied left-to-right without precedence rules.

    Supported Operators:
        - '+' : Addition
        - '*' : Multiplication
        - '||': Concatenation (combines digits into a single number)

    Example:
        Numbers: [6, 8, 6]
        Operators: ['*', '||']
        Evaluation: (6 * 8) || 6 -> 48 || 6 -> 486

    :param numbers: List of numbers in the equation.
    :param ops: List of operators ('+', '*', '||') to apply between the numbers.
    :return: Result of evaluating the expression.
    """
    result = numbers[0]
    for i in range(len(ops)):
        if ops[i] == '+':
            result += numbers[i + 1]
        elif ops[i] == '*':
            result *= numbers[i + 1]
        elif ops[i] == '||':
            # Concatenate the digits of the two numbers
            result = int(str(result) + str(numbers[i + 1]))
    return result

def can_form_target(target, numbers, allowed_ops):
    """
    Determines if a target value can be formed by inserting allowed operators 
    (`+`, `*`, `||`) between the numbers in left-to-right order.

    This function uses recursion to explore all possible operator combinations,
    with memoization to avoid redundant calculations.

    :param target: Target value for the equation.
    :param numbers: List of numbers in the equation.
    :param allowed_ops: List of allowed operators (e.g., ['+', '*'] for Part 1).
    :return: True if the target can be formed, False otherwise.
    """
    def helper(index, current_value):
        # Base case: If we've processed all numbers, check if we hit the target
        if index == len(numbers):
            return current_value == target

        # Memoization key
        key = (index, current_value)
        if key in memo:
            return memo[key]

        # Try all allowed operators with the next number
        for op in allowed_ops:
            if op == '+':
                next_value = current_value + numbers[index]
            elif op == '*':
                next_value = current_value * numbers[index]
            elif op == '||':
                next_value = int(str(current_value) + str(numbers[index]))

            # Recurse to process the next number
            if helper(index + 1, next_value):
                memo[key] = True
                return True

        # If no combination works, store False in memo and return
        memo[key] = False
        return False

    # Initialize memoization dictionary and start recursion
    memo = {}
    return helper(1, numbers[0])

def calculate_total_calibration(file_path, allowed_ops):
    """
    Calculates the total calibration result by summing up all valid test values,
    considering only the specified allowed operators.

    Example for Part 1:
        Allowed Operators: ['+', '*']
    
    Example for Part 2:
        Allowed Operators: ['+', '*', '||']

    :param file_path: Path to the input file (e.g., "input.txt").
    :param allowed_ops: List of allowed operators for validation.
                        ['+', '*'] for Part 1 or ['+', '*', '||'] for Part 2.
    :return: Total calibration result (sum of valid test values).
    """
    equations = read_input(file_path)
    total_calibration = 0
    
    for target, numbers in equations:
        # Check if this equation is valid using recursive function with memoization
        if can_form_target(target, numbers, allowed_ops):
            total_calibration += target
    
    return total_calibration

def test_example():
    """
    Tests both Part 1 and Part 2 logic using the example provided in the puzzle description.

    Example Input:
        [
            (190, [10, 19]),
            (3267, [81, 40, 27]),
            (83, [17, 5]),
            (156, [15, 6]),
            (7290, [6, 8, 6, 15]),
            (161011, [16, 10, 13]),
            (192, [17, 8, 14]),
            (21037, [9, 7, 18, 13]),
            (292, [11, 6, 16, 20])
        ]

    Expected Results:
        - Part 1 Result: Sum of valid test values using `+` and `*`: `3749`
        - Part 2 Result: Sum of valid test values using `+`, `*`, and `||`: `11387`
    
    :return: None
    """
    
    example_data = [
        (190, [10, 19]),
        (3267, [81, 40, 27]),
        (83, [17, 5]),
        (156, [15, 6]),
        (7290, [6, 8, 6, 15]),
        (161011, [16, 10, 13]),
        (192, [17, 8, 14]),
        (21037, [9, 7, 18, 13]),
        (292, [11, 6, 16, 20])
    ]

    # Calculate results for both parts using example data
    part_1_result = sum(target for target, nums in example_data if can_form_target(target=target,
                                                                                  numbers=nums,
                                                                                  allowed_ops=['+', '*']))
    
    part_2_result = sum(target for target, nums in example_data if can_form_target(target=target,
                                                                                  numbers=nums,
                                                                                  allowed_ops=['+', '*', '||']))
    
    print(f"Test Example - Part 1 Result: {part_1_result} (Expected: {3749})")
    print(f"Test Example - Part 2 Result: {part_2_result} (Expected: {11387})")

if __name__ == "__main__":
    # Input file containing the equations
    input_file = "input.txt"

    # Run tests first using example data from puzzle description
    print("Running Test Example...")
    test_example()
    
    # Part 1: Only addition (+) and multiplication (*) are allowed
    part_1_result = calculate_total_calibration(input_file, allowed_ops=['+', '*'])
    
    # Part 2: Addition (+), multiplication (*), and concatenation (||) are allowed
    part_2_result = calculate_total_calibration(input_file, allowed_ops=['+', '*', '||'])
    
    # Print results for both parts
    print(f"Part 1 - Total Calibration Result (using + and *): {part_1_result}")
    print(f"Part 2 - Total Calibration Result (using +, *, and ||): {part_2_result}")