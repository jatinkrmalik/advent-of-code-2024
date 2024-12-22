from collections import defaultdict
from typing import List, Tuple

def calculate_antinodes(grid: List[str]) -> Tuple[int, List[str]]:
    """
    Calculates the number of unique antinode locations in a grid of antennas.
    Antinodes are formed by collinear antennas of the same frequency where
    one antenna is twice as far from the antinode as another antenna.

    Args:
        grid: A list of strings representing the antenna map.
              '.' denotes empty space, and alphanumeric characters represent antennas.

    Returns:
        A tuple containing:
            - The number of unique antinode locations.
            - A modified grid with antinodes marked by '#'.
    """

    rows = len(grid)
    cols = len(grid[0])
    antenna_locations = defaultdict(list)  # {frequency: [(row, col), ...]}
    antinode_locations = set()  # {(row, col), ...}

    # 1. Record antenna locations for each frequency
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell != '.':
                antenna_locations[cell].append((row_index, col_index))

    modified_grid = [list(row) for row in grid]  # Copy grid to mark antinodes

    # 2. Process each frequency to find antinodes
    for frequency, locations in antenna_locations.items():
        num_antennas = len(locations)

        # 3. Check for antinodes formed by pairs of antennas
        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                r1, c1 = locations[i]  # Antenna 1
                r2, c2 = locations[j]  # Antenna 2

                # Calculate potential antinode locations
                row_diff, col_diff = r2 - r1, c2 - c1
                # Antinode where Antenna 1 is closer
                antinode1 = (r1 - row_diff, c1 - col_diff)
                # Antinode where Antenna 2 is closer
                antinode2 = (r2 + row_diff, c2 + col_diff)

                # Check if potential antinodes are valid and mark them
                for antinode_r, antinode_c in [antinode1, antinode2]:
                    if 0 <= antinode_r < rows and 0 <= antinode_c < cols:
                        if is_valid_antinode(r1, c1, r2, c2, antinode_r, antinode_c):
                            antinode_locations.add((antinode_r, antinode_c))
                            mark_antinode(modified_grid, antinode_r, antinode_c)

        # 4. Check for antinodes formed by three or more antennas (trios)
        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                for k in range(j + 1, num_antennas):
                    r1, c1 = locations[i]  # Antenna 1
                    r2, c2 = locations[j]  # Antenna 2
                    r3, c3 = locations[k]  # Antenna 3 (potential antinode)

                    if is_antinode_from_trio(r1, c1, r2, c2, r3, c3):
                        if 0 <= r3 < rows and 0 <= c3 < cols:
                            antinode_locations.add((r3, c3))
                            mark_antinode(modified_grid, r3, c3)

    return len(antinode_locations), ["".join(row) for row in modified_grid]

def is_valid_antinode(r1: int, c1: int, r2: int, c2: int, antinode_r: int, antinode_c: int) -> bool:
    """
    Checks if a given point is a valid antinode formed by two antennas.
    The antinode is valid if one antenna is twice as far from it as the other.

    Args:
        r1, c1: Coordinates of the first antenna.
        r2, c2: Coordinates of the second antenna.
        antinode_r, antinode_c: Coordinates of the potential antinode.

    Returns:
        True if the point is a valid antinode, False otherwise.
    """
    dist_sq_1 = (r1 - antinode_r) ** 2 + (c1 - antinode_c) ** 2  # Squared distance to Antenna 1
    dist_sq_2 = (r2 - antinode_r) ** 2 + (c2 - antinode_c) ** 2  # Squared distance to Antenna 2
    dist_sq_between = (r2 - r1) ** 2 + (c2 - c1) ** 2  # Squared distance between antennas

    return dist_sq_1 == dist_sq_between or dist_sq_2 == dist_sq_between

def is_antinode_from_trio(r1: int, c1: int, r2: int, c2: int, r3: int, c3: int) -> bool:
    """
    Checks if an antenna at (r3, c3) is an antinode formed by three antennas.
    It is an antinode if it's collinear with the other two and one of the other
    antennas is twice as far from it as the remaining antenna.

    Args:
        r1, c1: Coordinates of the first antenna.
        r2, c2: Coordinates of the second antenna.
        r3, c3: Coordinates of the third antenna (potential antinode).

    Returns:
        True if (r3, c3) is an antinode formed by the trio, False otherwise.
    """

    # Squared distances between antennas
    dist_sq_12 = (r1 - r2) ** 2 + (c1 - c2) ** 2
    dist_sq_13 = (r1 - r3) ** 2 + (c1 - c3) ** 2
    dist_sq_23 = (r2 - r3) ** 2 + (c2 - c3) ** 2

    # Check collinearity and distance conditions
    # The third antenna (r3, c3) can be an antinode if:
    # 1. The distance between (r1, c1) and (r3, c3) is 4 times the distance between (r1, c1) and (r2, c2)
    # 2. The distance between (r1, c1) and (r3, c3) is 1/4 the distance between (r1, c1) and (r2, c2)
    # 3. The distance between (r2, c2) and (r3, c3) is 4 times the distance between (r1, c1) and (r2, c2)
    # 4. The distance between (r2, c2) and (r3, c3) is 1/4 the distance between (r1, c1) and (r2, c2)

    return (
        4 * dist_sq_13 == dist_sq_12
        or dist_sq_13 == 4 * dist_sq_12
        or 4 * dist_sq_23 == dist_sq_12
        or dist_sq_23 == 4 * dist_sq_12
    )

def mark_antinode(grid: List[List[str]], row: int, col: int):
    """Marks an antinode on the grid if the cell is empty."""
    if grid[row][col] == '.':
        grid[row][col] = '#'

def calculate_antinodes_with_harmonics(grid: List[str]) -> Tuple[int, List[str]]:
    """
    Calculates the number of unique antinode locations in a grid of antennas,
    considering resonant harmonics. With harmonics, an antinode occurs at any
    grid position exactly in line with at least two antennas of the same frequency,
    regardless of distance.

    Args:
        grid: A list of strings representing the antenna map.
              '.' denotes empty space, and alphanumeric characters represent antennas.

    Returns:
        A tuple containing:
            - The number of unique antinode locations.
            - A modified grid with antinodes marked by '#'.
    """

    rows = len(grid)
    cols = len(grid[0])
    antenna_locations = defaultdict(list)  # {frequency: [(row, col), ...]}
    antinode_locations = set()  # {(row, col), ...}

    # 1. Record antenna locations for each frequency
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell != '.':
                antenna_locations[cell].append((row_index, col_index))

    modified_grid = [list(row) for row in grid]  # Copy grid to mark antinodes

    # 2. Process each frequency to find antinodes
    for frequency, locations in antenna_locations.items():
        num_antennas = len(locations)

        # If only one antenna of this frequency, it can't be an antinode
        if num_antennas < 2:
            continue

        # Mark all antennas of this frequency as antinodes
        for r, c in locations:
            antinode_locations.add((r, c))
            mark_antinode(modified_grid, r, c)
        
        # 3. Find all points collinear with at least two antennas
        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                r1, c1 = locations[i]
                r2, c2 = locations[j]

                # Iterate through all points on the grid
                for r in range(rows):
                    for c in range(cols):
                        # Skip the antenna locations themselves
                        if (r, c) == (r1, c1) or (r, c) == (r2, c2):
                            continue

                        # Check for collinearity using cross-product formula
                        if is_collinear(r1, c1, r2, c2, r, c):
                            antinode_locations.add((r, c))
                            mark_antinode(modified_grid, r, c)
    
    
    for frequency, locations in antenna_locations.items():
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                r1, c1 = locations[i]
                r2, c2 = locations[j]

                # Calculate the step for traversing the line
                row_step = r2 - r1
                col_step = c2 - c1

                # Ensure that we don't divide by zero
                if row_step == 0 and col_step == 0:
                    continue

                # Find the greatest common divisor (GCD) to simplify the step
                def gcd(a, b):
                    while b:
                        a, b = b, a % b
                    return a

                divisor = gcd(row_step, col_step)
                row_step //= divisor
                col_step //= divisor
                
                # Start from the first antenna and move along the line
                r, c = r1 + row_step, c1 + col_step

                # Continue until we are within grid boundaries
                while 0 <= r < rows and 0 <= c < cols:
                    # If this point is not already marked as an antinode, mark it
                    if (r,c) != (r1,c1) and (r,c) != (r2, c2) and is_collinear(r1,c1, r2, c2, r, c):
                        antinode_locations.add((r, c))
                        mark_antinode(modified_grid, r, c)

                    # Move to the next point on the line
                    r += row_step
                    c += col_step

                # Start from the first antenna and move along the line in the opposite direction
                r, c = r1 - row_step, c1 - col_step

                # Continue until we are within grid boundaries
                while 0 <= r < rows and 0 <= c < cols:
                    # If this point is not already marked as an antinode, mark it
                    if (r,c) != (r1,c1) and (r,c) != (r2, c2) and is_collinear(r1,c1, r2, c2, r, c):
                        antinode_locations.add((r, c))
                        mark_antinode(modified_grid, r, c)
                    
                    # Move to the next point on the line
                    r -= row_step
                    c -= col_step

    return len(antinode_locations), ["".join(row) for row in modified_grid]

def is_collinear(r1: int, c1: int, r2: int, c2: int, r: int, c: int) -> bool:
    """
    Checks if a point (r, c) is collinear with two other points (r1, c1) and (r2, c2)
    using the cross-product formula.

    Args:
        r1, c1: Coordinates of the first point.
        r2, c2: Coordinates of the second point.
        r, c:   Coordinates of the point to check for collinearity.

    Returns:
        True if the point is collinear, False otherwise.
    """
    return (c2 - c1) * (r - r1) == (c - c1) * (r2 - r1)

def solve_test_cases():
    """
    Solves the provided test cases, asserts the results, and prints the modified grids.
    """
    test_cases = [
        # (
        #     [
        #         "............",
        #         "........0...",
        #         ".....0......",
        #         ".......0....",
        #         "....0.......",
        #         "......A.....",
        #         "............",
        #         "............",
        #         "........A...",
        #         ".........A..",
        #         "............",
        #         "............",
        #     ],
        #     14,
        #     34,
        # ),
        # (
        #     [
        #         "..........",
        #         "..........",
        #         "..........",
        #         "....a.....",
        #         "..........",
        #         ".....a....",
        #         "..........",
        #         "..........",
        #         "..........",
        #         "..........",
        #     ],
        #     2,
        #     5
        # ),
        #  (
        #     [
        #         "..........",
        #         "..........",
        #         "..........",
        #         "....a.....",
        #         "........a.",
        #         ".....a....",
        #         "..........",
        #         "......A...",
        #         "..........",
        #         "..........",
        #     ],
        #     3,
        #     6
        # ),
        (
            [
                "T.........",
                "...T......",
                ".T........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
            ],
            9
        )
    ]

    for grid, expected in test_cases:
        # num_antinodes, modified_grid = calculate_antinodes(grid)
        num_antinodes_part2, modified_grid_part2 = calculate_antinodes_with_harmonics(grid)
        # print(f"Input:\n{grid}")
        # print(f"Part 1 - Expected Antinodes: {expected}, Got: {num_antinodes}")
        # print("Part 1 - Modified Grid:")
        # for row in modified_grid:
        #     print(row)
        # print("-" * 20)
        # assert num_antinodes == expected
        print(f"Part 2 - Expected Antinodes: {expected}, Got: {num_antinodes_part2}")
        # print("Part 2 - Modified Grid:")
        # for row in modified_grid_part2:
        #     print(row)
        # print("-" * 20)
        assert num_antinodes_part2 == expected
    print("All test cases passed!")


if __name__ == "__main__":
    solve_test_cases()  # Run the provided test cases first

    filepath = "day_8/input.txt"
    with open(filepath, 'r') as file:
        grid = [line.strip() for line in file]

    num_antinodes, modified_grid = calculate_antinodes(grid)
    num_antinodes_part2, modified_grid_part2 = calculate_antinodes_with_harmonics(grid)

    # print(f"Input from {filepath}:")
    # for row in grid:
    #     print(row)
    print(f"Part 1 - Number of Antinodes: {num_antinodes}")
    # print("Part 1 - Modified Grid:")
    # for row in modified_grid:
    #     print(row)
    print(f"Part 2 - Number of Antinodes: {num_antinodes_part2}")
    # print("Part 2 - Modified Grid:")
    # for row in modified_grid_part2:
    #     print(row)