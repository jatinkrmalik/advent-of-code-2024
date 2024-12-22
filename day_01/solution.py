from collections import Counter

def read_input(file_path):
    """
    Reads the input file and returns a list of strings, each representing a line from the file.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def parse_columns(data):
    """
    Parses the input data into two lists of integers, representing location IDs from two different lists.
    
    Parameters:
    - data: List of strings where each string contains two integers separated by spaces.

    Returns:
    - tuple: Two lists of integers (list_a, list_b).
    """
    list_a, list_b = zip(*(map(int, line.split()) for line in data))
    return list(list_a), list(list_b)

def sum_of_difference(list_a, list_b):
    """
    Part 1: Calculate the total distance between two lists.
    
    The task is to pair up numbers from two lists (sorted independently) and sum their absolute differences.
    
    Parameters:
    - list_a: List of integers representing location IDs from the first historian's list.
    - list_b: List of integers representing location IDs from the second historian's list.

    Returns:
    - int: The total distance between the two lists.
    
    This helps determine how far apart the lists are when paired optimally.
    """
    # Sort both lists
    sorted_a = sorted(list_a)
    sorted_b = sorted(list_b)
    
    # Calculate sum of absolute differences between paired elements
    return sum(abs(a - b) for a, b in zip(sorted_a, sorted_b))

def calc_similarity_score(list_a, list_b):
    """
    Part 2: Calculate the similarity score between two lists.
    
    The task is to determine how often each number in the first list appears in the second list,
    and calculate a score by multiplying each number by its frequency in the second list.
    
    Parameters:
    - list_a: List of integers representing location IDs from the first historian's list.
    - list_b: List of integers representing location IDs from the second historian's list.

    Returns:
    - int: The similarity score based on common elements between the lists.
    
    This helps identify potential matches based on frequency of occurrence in both lists.
    """
    # Count occurrences of each number in list_b
    list_b_map = Counter(list_b)
    
    # Calculate similarity score by summing products of numbers and their frequencies in list_b
    return sum(a * list_b_map[a] for a in list_a)

if __name__ == "__main__":
    # Read and parse input data
    input_data = read_input('day_1/input.txt')
    
    # Parse columns into two separate lists
    list_a, list_b = parse_columns(input_data)
    
    # Part 1: Calculate and print the sum of differences
    total_distance = sum_of_difference(list_a, list_b)
    print("Day 1, Part 1: Total Distance =", total_distance)
    
    # Part 2: Calculate and print the similarity score
    similarity_score = calc_similarity_score(list_a, list_b)
    print("Day 1, Part 2: Similarity Score =", similarity_score)