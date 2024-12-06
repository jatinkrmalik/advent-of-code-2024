import threading
from time import time

def parse_input(file_path):
    """
    Reads the map from the input file and returns it as a list of strings.
    Each string represents a row in the map.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list[str]: The map as a list of strings.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]


def simulate_guard_patrol(map_data):
    """
    Simulates the guard's patrol based on the rules provided in Part 1.

    Args:
        map_data (list[str]): The lab map as a list of strings.

    Returns:
        int: The number of distinct positions visited by the guard.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # (row_offset, col_offset)
    current_direction = 0  # Start facing up
    visited_positions = set()

    for r, row in enumerate(map_data):
        for c, cell in enumerate(row):
            if cell == '^':
                guard_position = (r, c)

    print(f"Starting guard position: {guard_position}")
    visited_positions.add(guard_position)

    rows, cols = len(map_data), len(map_data[0])

    while True:
        next_row = guard_position[0] + directions[current_direction][0]
        next_col = guard_position[1] + directions[current_direction][1]

        if not (0 <= next_row < rows and 0 <= next_col < cols):
            print("Guard has left the mapped area.")
            break

        if map_data[next_row][next_col] == '#':
            current_direction = (current_direction + 1) % 4
            print(f"Obstacle ahead. Turning right. New direction index: {current_direction}")
        else:
            guard_position = (next_row, next_col)
            visited_positions.add(guard_position)
            print(f"Guard moved to: {guard_position}")

    return len(visited_positions)


def find_loop_positions_single_threaded(map_data):
    """
    Single-threaded function to find all possible positions where a new obstruction can be placed.
    
    Args:
        map_data (list[str]): The lab map as a list of strings.

    Returns:
        int: The number of valid positions where an obstruction can be placed.
    """
    def simulate_with_obstruction(obstruction_position):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        current_direction = 0

        modified_map = [list(row) for row in map_data]
        modified_map[obstruction_position[0]][obstruction_position[1]] = '#'

        visited_states = set()

        for r, row in enumerate(map_data):
            for c, cell in enumerate(row):
                if cell == '^':
                    guard_position = (r, c)

        while True:
            state = (guard_position, current_direction)
            if state in visited_states:
                return True
            visited_states.add(state)

            next_row = guard_position[0] + directions[current_direction][0]
            next_col = guard_position[1] + directions[current_direction][1]

            if not (0 <= next_row < len(modified_map) and 0 <= next_col < len(modified_map[0])):
                return False

            if modified_map[next_row][next_col] == '#':
                current_direction = (current_direction + 1) % 4
            else:
                guard_position = (next_row, next_col)

    candidate_positions = set()
    rows, cols = len(map_data), len(map_data[0])
    for r in range(rows):
        for c in range(cols):
            if map_data[r][c] == '.':
                neighbors = [
                    (r + dr, c + dc)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= r + dr < rows and 0 <= c + dc < cols
                ]
                if any(map_data[nr][nc] == '#' for nr, nc in neighbors):
                    candidate_positions.add((r, c))

    valid_positions = []
    for position in candidate_positions:
        if simulate_with_obstruction(position):
            valid_positions.append(position)

    print(f"Valid positions for obstructions: {valid_positions}")
    return len(valid_positions)


def find_loop_positions_multithreaded(map_data):
    """
    Multithreaded function to find all possible positions where a new obstruction can be placed
    to trap the guard in a loop.

    Args:
        map_data (list[str]): The lab map as a list of strings.

    Returns:
        int: The number of valid positions where an obstruction can be placed.
    """
    def simulate_with_obstruction(obstruction_position, results, index):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        current_direction = 0

        modified_map = [list(row) for row in map_data]
        modified_map[obstruction_position[0]][obstruction_position[1]] = '#'

        visited_states = set()
        
        for r, row in enumerate(map_data):
            for c, cell in enumerate(row):
                if cell == '^':
                    guard_position = (r, c)

        while True:
            state = (guard_position, current_direction)
            if state in visited_states:
                results[index] = True
                return
            visited_states.add(state)

            next_row = guard_position[0] + directions[current_direction][0]
            next_col = guard_position[1] + directions[current_direction][1]

            if not (0 <= next_row < len(modified_map) and 0 <= next_col < len(modified_map[0])):
                results[index] = False
                return

            if modified_map[next_row][next_col] == '#':
                current_direction = (current_direction + 1) % 4
            else:
                guard_position = (next_row, next_col)

    candidate_positions = set()
    rows, cols = len(map_data), len(map_data[0])
    for r in range(rows):
        for c in range(cols):
            if map_data[r][c] == '.':
                neighbors = [
                    (r + dr, c + dc)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= r + dr < rows and 0 <= c + dc < cols
                ]
                if any(map_data[nr][nc] == '#' for nr, nc in neighbors):
                    candidate_positions.add((r, c))

    print(f"Candidate positions for obstructions: {candidate_positions}")

    threads = []
    results = [None] * len(candidate_positions)
    candidate_positions = list(candidate_positions)

    for index, position in enumerate(candidate_positions):
        thread = threading.Thread(target=simulate_with_obstruction,
                                   args=(position, results, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    valid_positions = [candidate_positions[i] for i, result in enumerate(results) if result]
    print(f"Valid positions for obstructions: {valid_positions}")
    return len(valid_positions)


def measure_execution_time(map_data):
    """
    Measures and prints the execution time for both single-threaded and multithreaded approaches.

    Args:
        map_data (list[str]): The lab map as a list of strings.

    Returns:
        None
    """
    start_time = time()
    single_threaded_result = find_loop_positions_single_threaded(map_data)
    single_threaded_time = time() - start_time
    print(f"Single-threaded result: {single_threaded_result}, Time taken: {single_threaded_time:.2f} seconds")

    start_time = time()
    multithreaded_result = find_loop_positions_multithreaded(map_data)
    multithreaded_time = time() - start_time
    print(f"Multithreaded result: {multithreaded_result}, Time taken: {multithreaded_time:.2f} seconds")


if __name__ == "__main__":
    # Read input data
    map_data = parse_input('day_6/input.txt')    
    measure_execution_time(map_data)