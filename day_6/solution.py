# Advent of Code 2024 - Day 6: Guard Gallivant

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
    # Directions: up, right, down, left (clockwise order)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # (row_offset, col_offset)
    current_direction = 0  # Start facing up
    visited_positions = set()

    # Find initial guard position
    for r, row in enumerate(map_data):
        for c, cell in enumerate(row):
            if cell == '^':
                guard_position = (r, c)

    print(f"Starting guard position: {guard_position}")

    # Add starting position to visited positions
    visited_positions.add(guard_position)

    rows, cols = len(map_data), len(map_data[0])

    while True:
        # Calculate next position based on current direction
        next_row = guard_position[0] + directions[current_direction][0]
        next_col = guard_position[1] + directions[current_direction][1]

        # Check if next position is out of bounds
        if not (0 <= next_row < rows and 0 <= next_col < cols):
            print("Guard has left the mapped area.")
            break

        # Check if next position is blocked by an obstacle
        if map_data[next_row][next_col] == '#':
            # Turn right (90 degrees clockwise)
            current_direction = (current_direction + 1) % 4
            print(f"Obstacle ahead. Turning right. New direction index: {current_direction}")
        else:
            # Move forward
            guard_position = (next_row, next_col)
            visited_positions.add(guard_position)
            print(f"Guard moved to: {guard_position}")

    return len(visited_positions)


def find_loop_positions(map_data):
    """
    Finds all possible positions where a new obstruction can be placed to trap
    the guard in a loop.

    Args:
        map_data (list[str]): The lab map as a list of strings.

    Returns:
        int: The number of valid positions where an obstruction can be placed.
    """
    def simulate_with_obstruction(obstruction_position):
        """
        Simulates the guard's movement with an obstruction added at a specific position.
        
        Args:
            obstruction_position (tuple[int, int]): The position where an obstruction is added.
        
        Returns:
            bool: True if the guard gets stuck in a loop; False otherwise.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        current_direction = 0

        # Copy map data and add obstruction
        modified_map = [list(row) for row in map_data]
        modified_map[obstruction_position[0]][obstruction_position[1]] = '#'

        visited_states = set()
        
        # Find initial guard position
        for r, row in enumerate(map_data):
            for c, cell in enumerate(row):
                if cell == '^':
                    guard_position = (r, c)

        while True:
            state = (guard_position, current_direction)
            if state in visited_states:
                print(f"Loop detected with obstruction at {obstruction_position}")
                return True  # Loop detected
            visited_states.add(state)

            next_row = guard_position[0] + directions[current_direction][0]
            next_col = guard_position[1] + directions[current_direction][1]

            if not (0 <= next_row < len(modified_map) and 0 <= next_col < len(modified_map[0])):
                return False

            if modified_map[next_row][next_col] == '#':
                current_direction = (current_direction + 1) % 4
            else:
                guard_position = (next_row, next_col)

    valid_positions = set()
    
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if map_data[r][c] == '.' and not any(map_data[r][c] == '^' for row in map_data):
                print(f"Checking obstruction at position: {(r, c)}")
                if simulate_with_obstruction((r, c)):
                    valid_positions.add((r, c))
    
    print(f"Valid positions for obstructions: {valid_positions}")
    return len(valid_positions)


def main():
    """
    Main function to solve both parts of Day 6.
    """
    # Read input data
    map_data = parse_input('day_6/input.txt')

    # Solve Part 1
    print("=== Solving Part 1 ===")
    part_1_result = simulate_guard_patrol(map_data)
    print(f"Part 1: Distinct positions visited by the guard: {part_1_result}")

    # Solve Part 2
    print("\n=== Solving Part 2 ===")
    part_2_result = find_loop_positions(map_data)
    print(f"Part 2: Number of positions to place an obstruction: {part_2_result}")


def test():
    """
    Test function using the example provided in the problem statement.
    """
    example_map = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#..."
    ]

    print("=== Running Tests ===")
    
    part_1_test_result = simulate_guard_patrol(example_map)
    assert part_1_test_result == 41, f"Test failed for Part 1. Expected: 41, Got: {part_1_test_result}"
    
    part_2_test_result = find_loop_positions(example_map)
    assert part_2_test_result == 6, f"Test failed for Part 2. Expected: 6, Got: {part_2_test_result}"

    print("All tests passed!")


if __name__ == "__main__":
    test()   # Run tests first
    main()   # Solve actual puzzle