import re
from PIL import Image

class Robot:
    """
    Represents a single robot with its position and velocity.
    """
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update_position(self, width, height):
        """
        Updates the robot's position based on its velocity and applies wrapping.
        """
        self.x = (self.x + self.vx) % width
        self.y = (self.y + self.vy) % height

class Simulation:
    """
    Represents the simulation environment containing multiple robots.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.robots = []

    def add_robot(self, robot):
        self.robots.append(robot)

    def parse_input(self, lines):
        for line in lines:
            match = re.match(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)", line)
            if match:
                x, y, vx, vy = map(int, match.groups())
                self.add_robot(Robot(x, y, vx, vy))

    def simulate(self, time_steps, generate_images=False, image_dir="images", alignment_threshold=5):
        """
        Simulates the movement of all robots for a given number of time steps.

        Args:
            time_steps: The number of time steps to simulate.
            generate_images: A flag to indicate whether to generate images of the grid.
            image_dir: The directory to save the generated images.
            alignment_threshold: The minimum number of robots aligned to trigger image generation.
        """
        for t in range(time_steps):
            for robot in self.robots:
                robot.update_position(self.width, self.height)
            if generate_images:
                if self.generate_image_if_aligned(t, image_dir, alignment_threshold):
                    print(f"Generated image for timestep: {t}")

    def count_robots_in_quadrants(self):
        q1, q2, q3, q4 = 0, 0, 0, 0
        mid_x = self.width // 2
        mid_y = self.height // 2
        for robot in self.robots: 
            if robot.x < mid_x and robot.y < mid_y:
                q1 += 1
            elif robot.x > mid_x and robot.y < mid_y:
                q2 += 1
            elif robot.x < mid_x and robot.y > mid_y:
                q3 += 1
            elif robot.x > mid_x and robot.y > mid_y:
                q4 += 1
        return q1, q2, q3, q4

    def calculate_safety_factor(self):
        q1, q2, q3, q4 = self.count_robots_in_quadrants()
        return q1 * q2 * q3 * q4

    def print_grid(self):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for robot in self.robots:
            if 0 <= robot.x < self.width and 0 <= robot.y < self.height:
                if grid[robot.y][robot.x] == '.':
                    grid[robot.y][robot.x] = '1'
                else:
                    grid[robot.y][robot.x] = str(int(grid[robot.y][robot.x]) + 1)
        for row in grid:
            print(''.join(row)) 

    def generate_image_if_aligned(self, time_step, image_dir, alignment_threshold):
        """
        Generates an image of the grid if at least 'alignment_threshold' robots are aligned.

        Args:
            time_step: The current time step.
            image_dir: The directory to save the image.
            alignment_threshold: The minimum number of robots aligned to trigger image generation.
        """
        import os
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Check for horizontal alignment
        x_counts = {}
        for robot in self.robots:
            if robot.x not in x_counts:
                x_counts[robot.x] = []
            x_counts[robot.x].append(robot.y)

        for x, y_values in x_counts.items():
            y_values.sort()
            for i in range(len(y_values) - alignment_threshold + 1):
                if all(y_values[i+j] - y_values[i+j-1] == 1 for j in range(1, alignment_threshold)):
                    self.generate_image(time_step, image_dir)
                    return True

        # Check for vertical alignment
        y_counts = {}
        for robot in self.robots:
            if robot.y not in y_counts:
                y_counts[robot.y] = []
            y_counts[robot.y].append(robot.x)

        for y, x_values in y_counts.items():
            x_values.sort()
            for i in range(len(x_values) - alignment_threshold + 1):
                if all(x_values[i+j] - x_values[i+j-1] == 1 for j in range(1, alignment_threshold)):
                    self.generate_image(time_step, image_dir)
                    return True

        return False

    def generate_image(self, time_step, image_dir):
        """
        Generates an image of the grid at the current time step.

        Args:
            time_step: The current time step.
            image_dir: The directory to save the image.
        """
        import os
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        image = Image.new("RGB", (self.width, self.height), "white")
        pixels = image.load()

        for robot in self.robots:
            if 0 <= robot.x < self.width and 0 <= robot.y < self.height:
                pixels[robot.x, robot.y] = (0, 0, 0)  # Black pixel for robot

        image.save(f"{image_dir}/grid_{time_step:05d}.png")

def test_solution():
    test_input = [
        "p=0,4 v=3,-3",
        "p=6,3 v=-1,-3",
        "p=10,3 v=-1,2",
        "p=2,0 v=2,-1",
        "p=0,0 v=1,3",
        "p=3,0 v=-2,-2",
        "p=7,6 v=-1,-3",
        "p=3,0 v=-1,-2",
        "p=9,3 v=2,3",
        "p=7,3 v=-1,2",
        "p=2,4 v=2,-3",
        "p=9,5 v=-3,-3",
    ]
    simulation = Simulation(11, 7)
    simulation.parse_input(test_input)
    simulation.simulate(100)
    simulation.print_grid()
    safety_factor = simulation.calculate_safety_factor()
    assert safety_factor == 12, f"Expected 12, but got {safety_factor}"
    print("Test passed!")

if __name__ == "__main__":
    test_solution()

    try:
        with open("day_14/input.txt", "r") as f:
            lines = f.readlines()

        simulation = Simulation(101, 103)
        simulation.parse_input(lines)

        # Part 1
        simulation.simulate(100)
        safety_factor = simulation.calculate_safety_factor()
        print(f"Safety factor: {safety_factor}")

        # Part 2: Generate images selectively based on alignment
        simulation.simulate(100000, generate_images=True, image_dir="day_14/images_aligned", alignment_threshold=5)
        print("Images generated in the 'images_aligned' directory.")

    except FileNotFoundError:
        print("Error: input.txt not found.")