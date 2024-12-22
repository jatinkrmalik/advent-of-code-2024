# Day 3 - Mull It Over

import re
import time

def read_input(file_path):
    """
    Reads the content of the given file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r') as f:
        return f.read()

def process(mem_dump):
    """
    Processes the memory dump and calculates the sum of all mul(x, y) operations.

    Args:
        mem_dump (str): Memory dump string containing mul() operations.

    Returns:
        int: The total sum of all mul(x, y) operations.
    """
    pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    matches = pattern.findall(mem_dump)

    total_sum = 0
    for match in matches:
        nums = [int(num) for num in match[4:-1].split(',')]
        total_sum += nums[0] * nums[1]

    return total_sum

def parse_and_calculate_regex(memory):
    """
    Parses the memory dump using regex and calculates the conditional sum of mul(x, y) operations.

    The function respects the state changes triggered by do() and don't() instructions.

    Args:
        memory (str): Memory dump string containing mul(), do(), and don't() instructions.

    Returns:
        int: The conditional sum of mul(x, y) operations based on state changes.
    """
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")

    tokens = re.split(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", memory)

    mul_enabled = True
    total_sum = 0

    for token in tokens:
        token = token.strip()
        if not token:
            continue

        if do_pattern.fullmatch(token):
            mul_enabled = True
        elif dont_pattern.fullmatch(token):
            mul_enabled = False
        elif mul_pattern.fullmatch(token):
            if mul_enabled:
                x, y = map(int, mul_pattern.match(token).groups())
                total_sum += x * y

    return total_sum

def parse_and_calculate_linearly(memory):
    """
    Parses the memory dump linearly and calculates the conditional sum of mul(x, y) operations.

    The function respects the state changes triggered by do() and don't() instructions
    while processing the memory string character by character.

    Args:
        memory (str): Memory dump string containing mul(), do(), and don't() instructions.

    Returns:
        int: The conditional sum of mul(x, y) operations based on state changes.
    """
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    mul_enabled = True
    total_sum = 0

    i = 0
    while i < len(memory):
        if memory[i:i+3] == "do(":
            mul_enabled = True
            i += 4  # Skip past "do()"
        elif memory[i:i+6] == "don't(":
            mul_enabled = False
            i += 7  # Skip past "don't()"
        elif memory[i:i+4] == "mul(":
            match = mul_pattern.match(memory[i:])
            if match and mul_enabled:
                x, y = map(int, match.groups())
                total_sum += x * y
            if match:
                i += match.end()  # Skip past the matched "mul(x,y)"
            else:
                i += 1  # Move forward if not a valid mul()
        else:
            i += 1  # Move forward for any other character

    return total_sum

if __name__ == '__main__':
    """
    Main execution flow of the program.

    - Reads the input memory dump from 'day_3/input.txt'.
    - Computes the unconditional sum of all mul(x, y) operations (Part 1).
    - Computes the conditional sum using both linear and regex-based methods (Part 2).
    - Measures and displays the execution times for both methods.
    """
    mem_dump = read_input("day_3/input.txt")

    # Part 1: Calculate the sum of all mul() operations unconditionally
    sum = process(mem_dump)
    print("Part 1: ", sum)

    # Part 2: Calculate the conditional sum linearly
    start_time = time.time()
    conditional_sum_linear = parse_and_calculate_linearly(mem_dump)
    linear_time = time.time() - start_time
    print("Part 2 (Linear): ", conditional_sum_linear)
    print("Linear function took {:.6f} seconds".format(linear_time))

    # Part 2: Calculate the conditional sum using regex
    start_time = time.time()
    conditional_sum_regex = parse_and_calculate_regex(mem_dump)
    regex_time = time.time() - start_time
    print("Part 2 (Regex): ", conditional_sum_regex)
    print("Regex function took {:.6f} seconds".format(regex_time))