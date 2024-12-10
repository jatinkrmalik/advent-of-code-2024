from collections import deque
from typing import List, Set, Tuple, Dict

def read_topographic_map(filename: str) -> List[List[int]]:
    """
    Read the topographic map from input file and convert to 2D grid of integers.
    Each position represents height from 0 (lowest) to 9 (highest).
    """
    with open(filename, 'r') as f:
        return [[int(char) for char in line.strip()] for line in f]

def grid_from_string(input_str: str) -> List[List[int]]:
    """
    Convert a string representation of grid to 2D list of integers.
    Ignores '.' characters which represent impassable tiles in examples.
    """
    return [[int(char) if char != '.' else -1 
             for char in line.strip()] 
             for line in input_str.strip().split('\n')]

def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Find all positions with height 0 (trailheads) in the grid.
    Returns list of (row, col) coordinates.
    """
    rows, cols = len(grid), len(grid[0])
    return [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

def get_valid_neighbors(grid: List[List[int]], row: int, col: int, 
                       current_height: int) -> List[Tuple[int, int]]:
    """
    Get all valid neighboring positions that are exactly one height higher.
    Valid moves are up, down, left, right (no diagonals).
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check bounds and height increment
        if (0 <= new_row < rows and 0 <= new_col < cols and 
            grid[new_row][new_col] == current_height + 1):
            neighbors.append((new_row, new_col))
    return neighbors

# Part 1 Methods
def count_reachable_peaks(grid: List[List[int]], start_row: int, 
                         start_col: int) -> int:
    """
    Count number of height-9 positions reachable from given trailhead
    via valid hiking trails (increasing by exactly 1 at each step).
    Uses BFS to find all possible paths.
    """
    reached_peaks = set()  # Store unique peak positions
    queue = deque([(start_row, start_col, 0)])  # (row, col, current_height)
    
    while queue:
        row, col, height = queue.popleft()
        
        # If we reached a peak, add it to our set
        if height == 9:
            reached_peaks.add((row, col))
            continue
            
        # Get valid next positions (exactly one height higher)
        for next_row, next_col in get_valid_neighbors(grid, row, col, height):
            queue.append((next_row, next_col, height + 1))
    
    return len(reached_peaks)

def solve_part1(grid: List[List[int]]) -> int:
    """
    Solve Part 1: Sum of scores (number of reachable peaks) for all trailheads
    """
    trailheads = find_trailheads(grid)
    return sum(count_reachable_peaks(grid, row, col) 
              for row, col in trailheads)

def run_part1_tests():
    """
    Run all test cases from Part 1 of the problem
    """
    # Test case 1: Simple example with score 1
    test1 = """
0123
1234
8765
9876
"""
    assert solve_part1(grid_from_string(test1)) == 1
    print("Test 1 passed!")

    # Test case 2: Example with score 2
    test2 = """
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
"""
    assert solve_part1(grid_from_string(test2)) == 2
    print("Test 2 passed!")

    # Test case 3: Example with score 4
    test3 = """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""
    assert solve_part1(grid_from_string(test3)) == 4
    print("Test 3 passed!")

    # Test case 4: Example with two trailheads (scores 1 and 2)
    test4 = """
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""
    assert solve_part1(grid_from_string(test4)) == 3
    print("Test 4 passed!")

    # Test case 5: Larger example with sum 36
    test5 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    assert solve_part1(grid_from_string(test5)) == 36
    print("Test 5 passed!")

    print("All Part 1 tests passed!")

# Part 2 Methods
def count_distinct_trails(grid: List[List[int]], start_row: int, 
                         start_col: int) -> int:
    """
    Count number of distinct hiking trails from a trailhead.
    A trail is distinct if it follows a different path, even to the same endpoint.
    Uses DFS with backtracking to count all possible paths.
    """
    def dfs(row: int, col: int, height: int) -> int:
        # Base case: reached a peak
        if height == 9:
            return 1
            
        total_paths = 0
        # Try all valid next steps
        for next_row, next_col in get_valid_neighbors(grid, row, col, height):
            total_paths += dfs(next_row, next_col, height + 1)
            
        return total_paths
    
    return dfs(start_row, start_col, 0)

def solve_part2(grid: List[List[int]]) -> int:
    """
    Solve Part 2: Sum of ratings (number of distinct trails) for all trailheads
    """
    trailheads = find_trailheads(grid)
    return sum(count_distinct_trails(grid, row, col) 
              for row, col in trailheads)

def run_part2_tests():
    """
    Run all test cases from Part 2 of the problem
    """
    # Test case 1: Single trailhead with 3 distinct paths
    test1 = """
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""
    assert solve_part2(grid_from_string(test1)) == 3
    print("Test 1 passed!")

    # Test case 2: Single trailhead with 13 distinct paths
    test2 = """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""
    assert solve_part2(grid_from_string(test2)) == 13
    print("Test 2 passed!")

    # Test case 3: Single trailhead with 227 distinct paths
    test3 = """
012345
123456
234567
345678
4.6789
56789.
"""
    assert solve_part2(grid_from_string(test3)) == 227
    print("Test 3 passed!")

    # Test case 4: Larger example with sum 81
    test4 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    assert solve_part2(grid_from_string(test4)) == 81
    print("Test 4 passed!")

    print("All Part 2 tests passed!")

if __name__ == "__main__":
    # First run the tests 
    print("Running Part 1 tests...")
    run_part1_tests()
    
    # Then solve the actual puzzle
    print("\nSolving puzzle input...")
    grid = read_topographic_map('day_10/input.txt')
    
    part1_result = solve_part1(grid)
    print(f"Part 1 - Sum of trailhead scores: {part1_result}")

    # First run the tests 
    print("\nRunning Part 2 tests...")
    run_part2_tests()

    # Then solve the actual puzzle
    print("\nSolving puzzle input...")
    grid = read_topographic_map('day_10/input.txt')
    
    part2_result = solve_part2(grid)
    print(f"Part 2 - Sum of trailhead ratings: {part2_result}")
