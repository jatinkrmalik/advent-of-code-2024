import heapq

class Reindeer:
    """Represents the Reindeer with its position and direction."""

    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction  # 0: North, 1: East, 2: South, 3: West

    def move_forward(self):
        """Calculates the new position when moving forward."""
        dr, dc = [(-1, 0), (0, 1), (1, 0), (0, -1)][self.direction]
        return self.row + dr, self.col + dc

    def turn_clockwise(self):
        """Returns the new direction after turning clockwise."""
        return (self.direction + 1) % 4

    def turn_counterclockwise(self):
        """Returns the new direction after turning counterclockwise."""
        new_direction = (self.direction - 1) % 4
        return new_direction if new_direction >= 0 else new_direction + 4

class State:
    """Represents a state in the search, including the Reindeer and the score."""

    def __init__(self, reindeer, score):
        self.reindeer = reindeer
        self.score = score

    def __lt__(self, other):
        """For priority queue ordering (lowest score first)."""
        return self.score < other.score

    def __eq__(self, other):
        return (self.reindeer.row, self.reindeer.col, self.reindeer.direction) == \
               (other.reindeer.row, other.reindeer.col, other.reindeer.direction)

    def __hash__(self):
        return hash((self.reindeer.row, self.reindeer.col, self.reindeer.direction))

class Maze:
    """Represents the maze grid and provides methods to solve it."""

    def __init__(self, grid):
        self.grid = grid
        self.start = None
        self.end = None
        self._find_start_and_end()

    def _find_start_and_end(self):
        """Finds the start and end positions in the grid."""
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'S':
                    self.start = (r, c)
                elif cell == 'E':
                    self.end = (r, c)
            if self.start and self.end:
                break

    def is_valid_position(self, row, col):
        """Checks if a position is valid within the grid."""
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]) and self.grid[row][col] != '#'

    def solve(self):
        """
        Finds the lowest score to reach the end tile from the start tile.

        Returns:
            The lowest score, or None if no path is found.
        """
        start_reindeer = Reindeer(self.start[0], self.start[1], 1)  # Start facing East
        start_state = State(start_reindeer, 0)

        queue = [start_state]
        visited = {start_state: 0}  # Store minimum score for each visited state

        while queue:
            current_state = heapq.heappop(queue)

            # Move forward
            new_row, new_col = current_state.reindeer.move_forward()
            if self.is_valid_position(new_row, new_col):
                new_reindeer = Reindeer(new_row, new_col, current_state.reindeer.direction)
                new_score = current_state.score + 1
                new_state = State(new_reindeer, new_score)

                if new_state not in visited or visited[new_state] > new_score:
                    visited[new_state] = new_score
                    heapq.heappush(queue, new_state)

            # Turn clockwise
            new_direction = current_state.reindeer.turn_clockwise()
            new_reindeer = Reindeer(current_state.reindeer.row, current_state.reindeer.col, new_direction)
            new_score = current_state.score + 1000
            new_state = State(new_reindeer, new_score)
            if new_state not in visited or visited[new_state] > new_score:
                visited[new_state] = new_score
                heapq.heappush(queue, new_state)

            # Turn counterclockwise
            new_direction = current_state.reindeer.turn_counterclockwise()
            new_reindeer = Reindeer(current_state.reindeer.row, current_state.reindeer.col, new_direction)
            new_score = current_state.score + 1000
            new_state = State(new_reindeer, new_score)
            if new_state not in visited or visited[new_state] > new_score:
                visited[new_state] = new_score
                heapq.heappush(queue, new_state)

        # Find the lowest score among all paths that reached the end
        min_score = float('inf')
        for state, score in visited.items():
            if (state.reindeer.row, state.reindeer.col) == self.end:
                min_score = min(min_score, score)

        return min_score if min_score != float('inf') else None

    def find_number_of_best_seats(self):
        """
        Finds the number of tiles that are part of at least one of the best paths.

        Returns:
            The number of best-path tiles.
        """
        lowest_score = self.solve()
        if lowest_score is None:
            return 0

        # 1. Calculate cost_to_end using backward Dijkstra's
        cost_to_end = {}
        for start_direction in range(4):  # All 4 directions
            start_reindeer = Reindeer(self.end[0], self.end[1], start_direction)
            start_state = State(start_reindeer, 0)
            queue = [start_state]
            visited = {start_state: 0}

            while queue:
                current_state = heapq.heappop(queue)
                cost_to_end[current_state] = current_state.score

                # Move backward (opposite of move_forward)
                for reverse_direction in [0, 1, 2, 3]:
                    dr, dc = [(-1, 0), (0, 1), (1, 0), (0, -1)][reverse_direction]
                    prev_row, prev_col = current_state.reindeer.row - dr, current_state.reindeer.col - dc
                    if self.is_valid_position(prev_row, prev_col):
                        prev_reindeer = Reindeer(prev_row, prev_col, (reverse_direction + 2) % 4)
                        prev_score = current_state.score + 1
                        prev_state = State(prev_reindeer, prev_score)

                        if prev_state not in visited or visited[prev_state] > prev_score:
                            visited[prev_state] = prev_score
                            heapq.heappush(queue, prev_state)

                # Turn (same as before, but cost is added to previous state)
                for turn_direction in [current_state.reindeer.turn_clockwise(), current_state.reindeer.turn_counterclockwise()]:
                    prev_reindeer = Reindeer(current_state.reindeer.row, current_state.reindeer.col, turn_direction)
                    prev_score = current_state.score + 1000
                    prev_state = State(prev_reindeer, prev_score)

                    if prev_state not in visited or visited[prev_state] > prev_score:
                        visited[prev_state] = prev_score
                        heapq.heappush(queue, prev_state)

        # 2. Find best-path tiles using the solve() method's visited states
        best_path_tiles = set()
        
        # Re-run solve() to get the visited states with minimum scores
        start_reindeer = Reindeer(self.start[0], self.start[1], 1)  # Start facing East
        start_state = State(start_reindeer, 0)
        queue = [start_state]
        visited = {start_state: 0}

        while queue:
            current_state = heapq.heappop(queue)

            # Move forward
            new_row, new_col = current_state.reindeer.move_forward()
            if self.is_valid_position(new_row, new_col):
                new_reindeer = Reindeer(new_row, new_col, current_state.reindeer.direction)
                new_score = current_state.score + 1
                new_state = State(new_reindeer, new_score)

                if new_state not in visited or visited[new_state] > new_score:
                    visited[new_state] = new_score
                    heapq.heappush(queue, new_state)

            # Turn clockwise
            new_direction = current_state.reindeer.turn_clockwise()
            new_reindeer = Reindeer(current_state.reindeer.row, current_state.reindeer.col, new_direction)
            new_score = current_state.score + 1000
            new_state = State(new_reindeer, new_score)
            if new_state not in visited or visited[new_state] > new_score:
                visited[new_state] = new_score
                heapq.heappush(queue, new_state)

            # Turn counterclockwise
            new_direction = current_state.reindeer.turn_counterclockwise()
            new_reindeer = Reindeer(current_state.reindeer.row, current_state.reindeer.col, new_direction)
            new_score = current_state.score + 1000
            new_state = State(new_reindeer, new_score)
            if new_state not in visited or visited[new_state] > new_score:
                visited[new_state] = new_score
                heapq.heappush(queue, new_state)
        
        for state, score in visited.items():
            if (state.reindeer.row, state.reindeer.col) == self.end and score == lowest_score:
                continue
            if state in cost_to_end and score + cost_to_end[state] == lowest_score:
                best_path_tiles.add((state.reindeer.row, state.reindeer.col))

        return len(best_path_tiles)

def test_reindeer_maze_part2():
    """Test cases for Part 2."""

    example1 = [
        "###############",
        "#.......#....E#",
        "#.#.###.#.###.#",
        "#.....#.#...#.#",
        "#.###.#####.#.#",
        "#.#.#.......#.#",
        "#.#.#####.###.#",
        "#...........#.#",
        "###.#.#####.#.#",
        "#...#.....#.#.#",
        "#.#.#.###.#.#.#",
        "#.....#...#.#.#",
        "#.###.#.#.#.#.#",
        "#S..#.....#...#",
        "###############"
    ]

    example2 = [
        "#################",
        "#...#...#...#..E#",
        "#.#.#.#.#.#.#.#.#",
        "#.#.#.#...#...#.#",
        "#.#.#.#.###.#.#.#",
        "#...#.#.#.....#.#",
        "#.#.#.#.#.#####.#",
        "#.#...#.#.#.....#",
        "#.#.#####.#.###.#",
        "#.#.#.......#...#",
        "#.#.###.#####.###",
        "#.#.#...#.....#.#",
        "#.#.#.#####.###.#",
        "#.#.#.........#.#",
        "#.#.#.#########.#",
        "#S#.............#",
        "#################"
    ]

    maze1 = Maze(example1)
    maze2 = Maze(example2)

    assert maze1.find_number_of_best_seats() == 45
    assert maze2.find_number_of_best_seats() == 64
    print("All test cases for Part 2 passed!")

if __name__ == "__main__":
    test_reindeer_maze_part2()

    # with open("input.txt", "r") as f:
    #     grid = f.read().splitlines()

    # maze = Maze(grid)
    # lowest_score = maze.solve()
    # num_best_seats = maze.find_number_of_best_seats()

    # print(f"The lowest score for Part 1 is: {lowest_score}")
    # print(f"The number of best-path tiles for Part 2 is: {num_best_seats}")