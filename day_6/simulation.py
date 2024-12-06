import os
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def read_map(file_path):
    """
    Reads the map from the input file.

    :param file_path: Path to the file containing the map.
    :return: A 2D list representing the grid.
    """
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]


def print_grid(grid, frames):
    """
    Visualizes the current state of the grid using matplotlib and saves the animation.

    :param grid: A 2D list representing the grid.
    :param frames: A list of 2D lists representing the grid at each step.
    """
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        numeric_frame = [
            [
                1 if cell == "X" else 2 if cell == "#" else 3 if cell in "^>v<" else 0
                for cell in row
            ]
            for row in frame
        ]
        cmap = plt.cm.colors.ListedColormap(["white", "gray", "black", "red"])
        ax.imshow(numeric_frame, cmap=cmap)

    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False)
    ani.save(
        "/home/jatin/git/advent-of-code-2024/day_6/simulation.mp4",
        writer="ffmpeg",
        fps=60,
        dpi=300,
    )
    plt.close(fig)


def simulate_guard_patrol(grid):
    """
    Simulates the guard's patrol based on the given rules and prints the simulation.

    :param grid: A 2D list representing the grid.
    :return: The number of distinct positions visited by the guard.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # (row_delta, col_delta)
    direction_symbols = "^>v<"  # Representing the guard's facing direction
    direction_index = 0  # Start facing "up" (index 0 in directions)

    guard_row, guard_col = None, None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in direction_symbols:
                guard_row, guard_col = r, c
                direction_index = direction_symbols.index(cell)
                grid[r][c] = "X"  # Mark starting position as visited
                break
        if guard_row is not None:
            break

    if guard_row is None or guard_col is None:
        raise ValueError("Guard's starting position not found in the grid.")

    visited_positions = set()
    visited_positions.add((guard_row, guard_col))

    frames = []  # Initialize frames list
    frames.append([row[:] for row in grid])  # Add initial state to frames

    while True:
        # Print current state
        print(
            f"Guard at ({guard_row}, {guard_col}) facing {direction_symbols[direction_index]}"
        )

        # Compute next position based on the current direction
        delta_row, delta_col = directions[direction_index]
        next_row = guard_row + delta_row
        next_col = guard_col + delta_col

        # Check if next position is within bounds
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            if grid[next_row][next_col] != "#":
                print(f"Moving to ({next_row}, {next_col})")
                # Move forward
                grid[guard_row][guard_col] = "X"  # Mark current position as visited
                guard_row, guard_col = next_row, next_col
                visited_positions.add((guard_row, guard_col))
                grid[guard_row][guard_col] = direction_symbols[
                    direction_index
                ]  # Update guard's symbol
            else:
                print(f"Obstacle at ({next_row}, {next_col}), turning right")
                # Obstacle detected, turn right 90 degrees
                direction_index = (direction_index + 1) % 4
                grid[guard_row][guard_col] = direction_symbols[
                    direction_index
                ]  # Update guard's symbol
        else:
            print(f"Guard is leaving the mapped area from ({guard_row}, {guard_col})")
            # Guard leaves the mapped area
            grid[guard_row][guard_col] = "X"  # Mark last position as visited
            frames.append([row[:] for row in grid])
            break  # Exit the simulation loop

        # Add current state to frames
        frames.append([row[:] for row in grid])

    # Generate the animation
    print_grid(grid, frames)

    return len(visited_positions)


if __name__ == "__main__":
    input_file = "input.txt"
    lab_map = read_map(input_file)

    distinct_positions = simulate_guard_patrol(lab_map)

    # Wait for user input before displaying the result
    input("\nSimulation complete! Press Enter to see the final answer...")

    print(f"\nNumber of distinct positions visited: {distinct_positions}")
