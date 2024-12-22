from collections import deque

class Racetrack:
    """Represents the racetrack and provides methods to solve the puzzle."""

    def __init__(self, grid):
        """Initializes the Racetrack object.
        Args:
            grid (list[str]): A list of strings representing the racetrack map.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start_pos = self._find_char('S')  # Find the starting position 'S'
        self.end_pos = self._find_char('E')    # Find the ending position 'E'

    def _find_char(self, char):
        """Locates a specific character within the grid.
        Args:
            char (str): The character to search for ('S' or 'E').
        Returns:
            tuple[int, int]: The (row, column) of the character, or None if not found.
        """
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == char:
                    return r, c
        return None

    def _bfs_precompute_distances(self, start_node):
        """Performs Breadth-First Search (BFS) to calculate the shortest distance from a starting node to all other reachable nodes.
        Args:
            start_node (tuple[int, int]): The (row, column) of the starting node.
        Returns:
            dict[tuple[int, int], int]: A dictionary where keys are (row, column) tuples and values are the shortest distances from the start node.
        """
        distances = {(r, c): float('inf') for r in range(self.rows) for c in range(self.cols)}  # Initialize distances to infinity
        distances[start_node] = 0  # Distance from start to itself is 0

        queue = deque([(start_node[0], start_node[1], 0)])  # Queue for BFS: (row, col, distance)

        while queue:
            r, c, dist = queue.popleft()  # Dequeue the current node

            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible moves: right, left, down, up
            for dr, dc in moves:
                nr, nc = r + dr, c + dc  # Calculate the coordinates of the neighbor
                # Check if the neighbor is within the grid, not a wall, and not visited with a shorter path
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#' and distances[(nr, nc)] == float('inf'):
                    distances[(nr, nc)] = dist + 1  # Update the distance to the neighbor
                    queue.append((nr, nc, dist + 1))  # Enqueue the neighbor
        return distances

    def _bfs_precompute_distances_reversed(self, start_node):
        """Performs BFS to calculate the shortest distance from all reachable nodes to a target node.
        This is equivalent to running BFS on a reversed graph, finding distances "to" the target.
        Args:
            start_node (tuple[int, int]): The (row, column) of the target node (in this case, the end position).
        Returns:
            dict[tuple[int, int], int]: A dictionary where keys are (row, column) tuples and values are the shortest distances to the target node.
        """
        distances = {(r, c): float('inf') for r in range(self.rows) for c in range(self.cols)}
        distances[start_node] = 0

        queue = deque([(start_node[0], start_node[1], 0)])

        while queue:
            r, c, dist = queue.popleft()

            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#' and distances[(nr, nc)] == float('inf'):
                    distances[(nr, nc)] = dist + 1
                    queue.append((nr, nc, dist + 1))
        return distances

    def solve_part1(self, min_savings=100):
        """Solves Part 1 of the puzzle: Count cheats saving >= 100 picoseconds with a 2-picosecond cheat.
        The approach is to iterate through all possible 2-picosecond cheats and calculate their savings.
        """
        # Precompute shortest distances from start and to end to avoid redundant BFS calls
        dist_from_start = self._bfs_precompute_distances(self.start_pos)
        dist_to_end = self._bfs_precompute_distances_reversed(self.end_pos)

        shortest_time_no_cheat = dist_from_start[self.end_pos]  # Shortest path without cheating
        if shortest_time_no_cheat == float('inf'):
            return 0  # No path exists

        seen_cheats = set()  # Keep track of counted cheats to avoid duplicates
        count_savings = 0


        # Iterate through each cell to find potential starting points for a cheat
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != '#':  # Cheat can only start on a track cell
                    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible movement directions
                    # Simulate the first step of the 2-picosecond cheat (moving into a wall)
                    for dr1, dc1 in moves:
                        r1, c1 = r + dr1, c + dc1
                        if 0 <= r1 < self.rows and 0 <= c1 < self.cols and self.grid[r1][c1] == '#':
                            # Simulate the second step of the 2-picosecond cheat (moving back onto a track)
                            for dr2, dc2 in moves:
                                r2, c2 = r1 + dr2, c1 + dc2
                                if 0 <= r2 < self.rows and 0 <= c2 < self.cols and self.grid[r2][c2] != '#':
                                    # Define the cheat by its start and end positions
                                    cheat_start_pos = (r, c)
                                    cheat_end_pos = (r2, c2)

                                    # Ensure the cheat hasn't been counted before
                                    if (r, c, r2, c2) not in seen_cheats:
                                        # Calculate the total time taken with this cheat
                                        time_to_cheat_start = dist_from_start[cheat_start_pos]
                                        time_from_cheat_end_to_end = dist_to_end[cheat_end_pos]
                                        total_time_with_cheat = time_to_cheat_start + 2 + time_from_cheat_end_to_end
                                        saving = shortest_time_no_cheat - total_time_with_cheat  # Calculate the saving

                                        if saving >= min_savings:  # Check if the cheat saves at least $min_savings
                                            count_savings += 1
                                            seen_cheats.add((r, c, r2, c2))  # Mark the cheat as counted
        return count_savings

    def _bfs_through_walls_limited(self, start, max_steps):
        """Performs a BFS allowing movement through walls, up to a maximum number of steps.
        Used to simulate the cheating process in Part 2.
        Args:
            start (tuple[int, int]): The starting position of the cheat.
            max_steps (int): The maximum duration of the cheat in picoseconds.
        Returns:
            dict[tuple[int, int], int]: A dictionary where keys are reachable track cells and values are the time taken to reach them.
        """
        rows = self.rows
        cols = self.cols
        start_row, start_col = start

        queue = deque([(start_row, start_col, 0)])  # Queue for BFS: (row, col, time)
        visited = {}  # Keep track of visited cells and the time taken to reach them

        while queue:
            r, c, time = queue.popleft()

            # If the cell has been visited before with a shorter or equal time, skip
            if (r, c) in visited and visited[(r, c)] <= time:
                continue
            visited[(r, c)] = time

            if time >= max_steps:  # Stop if the maximum cheat duration is reached
                continue

            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                # Allow movement through walls during the cheat
                if 0 <= nr < rows and 0 <= nc < cols:
                    queue.append((nr, nc, time + 1))

        reachable_track_cells = {}
        # Filter visited cells to only include those that are track cells
        for (r, c), time in visited.items():
            if self.grid[r][c] != '#':
                reachable_track_cells[(r, c)] = time
        return reachable_track_cells

    def solve_part2(self, min_savings=100):
        """Solves Part 2 of the puzzle: Count cheats saving >= 100 picoseconds with a cheat lasting up to 20 picoseconds.
        Iterates through all possible cheat start positions and simulates cheats up to 20 picoseconds.
        """
        # Precompute shortest distances from start and to end
        dist_from_start = self._bfs_precompute_distances(self.start_pos)
        dist_to_end = self._bfs_precompute_distances_reversed(self.end_pos)

        shortest_time_no_cheat = dist_from_start[self.end_pos]
        if shortest_time_no_cheat == float('inf'):
            return 0

        count_savings = 0
        seen_cheats = set()  # Track counted cheats by their start and end positions

        # Iterate through each cell as a potential starting point for the cheat
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != '#':  # Cheat starts on a track cell
                    # Simulate cheating for up to 20 picoseconds
                    reachable_during_cheat = self._bfs_through_walls_limited((r, c), 20)
                    # For each reachable track cell after cheating
                    for (r_end_cheat, c_end_cheat), cheat_duration in reachable_during_cheat.items():
                        # Ensure the cheat hasn't been counted
                        if (r, c, r_end_cheat, c_end_cheat) not in seen_cheats:
                            # Calculate total time with the cheat
                            total_time_with_cheat = dist_from_start[(r, c)] + cheat_duration + dist_to_end[(r_end_cheat, c_end_cheat)]
                            saving = shortest_time_no_cheat - total_time_with_cheat  # Calculate saving

                            if saving >= min_savings:  # Check if saving is at least $
                                count_savings += 1
                                seen_cheats.add((r, c, r_end_cheat, c_end_cheat))  # Mark cheat as counted
        return count_savings

    def test_solve_part1(self):
        """Test case for Part 1."""
        test_grid = [
            "###############",
            "#...#...#.....#",
            "#.#.#.#.#.###.#",
            "#S#...#.#.#...#",
            "#######.#.#.###",
            "#######.#.#...#",
            "#######.#.###.#",
            "###..E#...#...#",
            "###.#######.###",
            "#...###...#...#",
            "#.#####.#.###.#",
            "#.#...#.#.#...#",
            "#.#.#.#.#.#.###",
            "#...#...#...###",
            "###############",
        ]
        racetrack = Racetrack(test_grid)
        expected_count = 44
        actual_count = racetrack.solve_part1(min_savings=2)  # Set min_saving to 0 to count all cheats
        assert actual_count == expected_count, f"Part 1 test failed: Expected {expected_count}, got {actual_count}"
        print("Part 1 test passed")

    def test_solve_part2(self):
        """Test case for Part 2."""
        test_grid = [
            "###############",
            "#...#...#.....#",
            "#.#.#.#.#.###.#",
            "#S#...#.#.#...#",
            "#######.#.#.###",
            "#######.#.#...#",
            "#######.#.###.#",
            "###..E#...#...#",
            "###.#######.###",
            "#...###...#...#",
            "#.#####.#.###.#",
            "#.#...#.#.#...#",
            "#.#.#.#.#.#.###",
            "#...#...#...###",
            "###############",
        ]
        racetrack = Racetrack(test_grid)
        expected_count = 285
        actual_count = racetrack.solve_part2(min_savings=50)  # Set min_saving to 50
        assert actual_count == expected_count, f"Part 2 test failed: Expected {expected_count}, got {actual_count}"
        print("Part 2 test passed")

def read_input(filename):
    """Reads the puzzle input from the specified file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def main():
    """Main function to execute the solutions."""
    grid = read_input("day_20/input.txt")  # Read the racetrack map from the input file
    racetrack = Racetrack(grid)  # Create a Racetrack object

    # Run test cases
    racetrack.test_solve_part1()
    racetrack.test_solve_part2()

    # Solve Part 1 and print the result
    count_part1 = racetrack.solve_part1()
    print(f"Part 1 Cheats Saving at Least 100 Picoseconds: {count_part1}")

    # Solve Part 2 and print the result
    count_part2 = racetrack.solve_part2()
    print(f"Part 2 Cheats Saving at Least 100 Picoseconds: {count_part2}")

if __name__ == "__main__":
    main()