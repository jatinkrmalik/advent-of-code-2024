from collections import defaultdict

def read_input_file(filename):
    """
    Reads the grid of letters from an input file.
    
    :param filename: Name of the file containing the input grid.
    :return: List of strings representing the grid.
    """
    with open(filename, 'r') as file:
        grid = [line.strip() for line in file]
    return grid

def find_word_occurrences(grid, word):
    """
    Finds all occurrences of the given word in all directions in the grid.
    
    :param grid: List of strings representing the grid.
    :param word: The word to search for.
    :return: The total count of occurrences of the word.
    """
    # Define all 8 possible directions
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1), # diagonal up-left
        (-1, 1)   # diagonal up-right
    ]
    
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    word_length = len(word)

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                # Check if the word fits starting from (i, j) in direction (dx, dy)
                if (0 <= i + (word_length - 1) * dx < rows) and (0 <= j + (word_length - 1) * dy < cols):
                    match = True
                    for k in range(word_length):
                        if grid[i + k * dx][j + k * dy] != word[k]:
                            match = False
                            break
                    if match:
                        count += 1
    return count

def count_xmas_cross_patterns(input_grid):
    """
    Counts the number of unique X-MAS cross patterns in the grid.
    
    An X-MAS cross pattern is defined as:
    - 'M' on one of the arms, 'A' at the center, and 'S' on the opposite arm.
    - The pattern can exist in multiple diagonal orientations.
    """
    # Initialize variables
    xmas_count = 0  # Final count of X-MAS patterns
    direction_checks = []  # Temporary storage for valid directions to check
    a_cross_dict = defaultdict(int)  # Tracks unique 'A' centers forming valid X-MAS patterns

    # Direction mappings for grid traversal
    direction_dict_y = {7:-1, 8:-1, 9:-1,
                        4:0 , 5:0 , 6:0 ,
                        1:+1, 2:+1, 3:+1}

    direction_dict_x = {7:-1, 8:0, 9:+1,
                        4:-1, 5:0, 6:+1,
                        1:-1, 2:0, 3:+1}

    # Iterate over each cell in the grid
    for y, row in enumerate(input_grid):
        for x, cell in enumerate(row):
            # Check if the cell contains 'M'
            if cell == "M":
                # Check all possible directions where 'A' can be adjacent to 'M'
                if x > 1 and y < len(input_grid) - 2:  # Down-back
                    if input_grid[y + 1][x - 1] == "A":
                        direction_checks.append(1)
                if x > 1 and y > 1:  # Up-back
                    if input_grid[y - 1][x - 1] == "A":
                        direction_checks.append(7)
                if x < len(row) - 2 and y < len(input_grid) - 2:  # Down-forward
                    if input_grid[y + 1][x + 1] == "A":
                        direction_checks.append(3)
                if x < len(row) - 2 and y > 1:  # Up-forward
                    if input_grid[y - 1][x + 1] == "A":
                        direction_checks.append(9)

                # Process all valid directions to check for 'S'
                while direction_checks:
                    direction = direction_checks.pop(0)

                    # Start at the position adjacent to 'A'
                    y_check = y + 2 * direction_dict_y[direction]
                    x_check = x + 2 * direction_dict_x[direction]

                    # If the opposite position contains 'S', record the 'A' center
                    if input_grid[y_check][x_check] == "S":
                        center_y = y_check - direction_dict_y[direction]
                        center_x = x_check - direction_dict_x[direction]
                        a_cross_dict[(center_y, center_x)] += 1

    # Count unique 'A' centers that form valid X-MAS crosses
    for count in a_cross_dict.values():
        if count >= 2:  # An 'A' must be part of at least two valid X-MAS patterns
            xmas_count += 1

    return xmas_count



def main():
    grid = read_input_file('day_4/input.txt')
    
    # Part One: Find all occurrences of "XMAS"
    word_occurrences = find_word_occurrences(grid, "XMAS")
    print("Part 1 // Occurrences of 'XMAS':", word_occurrences)
    
    # Part Two: Find all occurrences of "X-MAS"

    # Testcase in example
    # grid = [
    # ".M.S......",
    # "..A..MSMS.",
    # ".M.S.MAA..",
    # "..A.ASMSM.",
    # ".M.S.M....",
    # "..........",
    # "S.S.S.S.S.",
    # ".A.A.A.A..",
    # "M.M.M.M.M.",
    # ".........."]
    # print(count_xmas_cross_patterns(grid))  # Output should match the given example

    x_mas_occurrences = count_xmas_cross_patterns(grid)
    print("Part 2 // Occurrences of 'X-MAS':", x_mas_occurrences)

if __name__ == "__main__":
    main()