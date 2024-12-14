import sympy
import time

def parse_input(lines):
    """Parses the input lines into a list of machine parameters."""
    machines = []
    i = 0
    while i < len(lines):
        if lines[i]:  # Check if the line is not blank
            ax = int(lines[i].split("X+")[1].split(",")[0])
            ay = int(lines[i].split("Y+")[1])
            bx = int(lines[i + 1].split("X+")[1].split(",")[0])
            by = int(lines[i + 1].split("Y+")[1])
            prize_x = int(lines[i + 2].split("X=")[1].split(",")[0])
            prize_y = int(lines[i + 2].split("Y=")[1])
            machines.append((ax, ay, bx, by, prize_x, prize_y))
            i += 3
        else:
            i += 1

    return machines

def solve_machine(ax, ay, bx, by, prize_x, prize_y):
    """
    Solves the equations for a single claw machine using brute-force (Part 1).
    This does not work for Part 2 due to the large prize coordinates and the need for a more efficient solution.

    Args:
        ax: Change in X-coordinate when pressing button A.
        ay: Change in Y-coordinate when pressing button A.
        bx: Change in X-coordinate when pressing button B.
        by: Change in Y-coordinate when pressing button B.
        prize_x: X-coordinate of the prize.
        prize_y: Y-coordinate of the prize.

    Returns:
        The minimum cost to win the prize, or 0 if no solution exists.
    """
    min_cost = float('inf')
    for a in range(101):
        for b in range(101):
            if ax * a + bx * b == prize_x and ay * a + by * b == prize_y:
                min_cost = min(min_cost, 3 * a + b)
    return min_cost if min_cost != float('inf') else 0

def solve_machine_algebra(a_x, a_y, b_x, b_y, p_x, p_y):
    """
    Solves the equations for a single claw machine using algebraic methods (Part 2).

    Args:
        a_x: Change in X-coordinate when pressing button A.
        a_y: Change in Y-coordinate when pressing button A.
        b_x: Change in X-coordinate when pressing button B.
        b_y: Change in Y-coordinate when pressing button B.
        p_x: X-coordinate of the prize.
        p_y: Y-coordinate of the prize.

    Returns:
        The minimum cost to win the prize, or 0 if no solution exists.
    """
    try:
        # Calculate the potential solution for the number of times button A is pressed
        denominator = b_x * a_y - b_y * a_x
        if denominator == 0:
            return 0  # No solution if the denominator is zero

        solution_a = (b_x * p_y - b_y * p_x) // denominator
        if (b_x * p_y - b_y * p_x) % denominator != 0:
            return 0  # No integer solution for solution_a

        # Calculate the potential solution for the number of times button B is pressed
        solution_b = (p_y - solution_a * a_y) // b_y
        if (p_y - solution_a * a_y) % b_y != 0:
            return 0  # No integer solution for solution_b

        return solution_a * 3 + solution_b
    except ZeroDivisionError:
        return 0  # Return 0 if there is a division by zero error


def test():
    test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    machines = parse_input(test_input.splitlines())

    # Test Part 1
    expected_costs_part1 = [280, 0, 200, 0]
    for i, machine in enumerate(machines):
        cost = solve_machine(*machine)
        assert cost == expected_costs_part1[i], f"Test case {i+1} (Part 1) failed. Expected {expected_costs_part1[i]}, got {cost}"

    print("All test cases passed!")

if __name__ == "__main__":
    test()

    with open("day_13/input.txt") as f:
        lines = [line.strip() for line in f]

    # Part 1
    start_time = time.time()
    machines = parse_input(lines)
    total_cost_part1 = 0
    win_count_part1 = 0
    for machine in machines:
        cost = solve_machine(*machine)
        if cost != -1:
            total_cost_part1 += cost
            win_count_part1 += 1
    end_time = time.time()
    elapsed_time_part1 = end_time - start_time

    print("Part 1:")
    print(f"Fewest tokens to win all possible prizes: {total_cost_part1}")
    print(f"Number of prizes won: {win_count_part1}")
    print(f"Elapsed time: {elapsed_time_part1:.6f} seconds")

    # Part 2
    print("\nPart 2:")
    machines = parse_input(lines)  # Reset machines list
    total_cost_part2_ee = 0
    win_count_part2_ee = 0
    total_cost_part2_dp = 0
    win_count_part2_dp = 0

    start_time_ee = time.time()
    for machine in machines:
        ax, ay, bx, by, prize_x, prize_y = machine
        prize_x += 10000000000000
        prize_y += 10000000000000
        cost = solve_machine_algebra(ax, ay, bx, by, prize_x, prize_y)
        total_cost_part2_ee += cost
        win_count_part2_ee += 1
    end_time_ee = time.time()
    print(f"Fewest tokens to win all possible prizes: {total_cost_part2_ee}")
    print(f"Number of prizes won: {win_count_part2_ee}")
    print(f"Elapsed time: {end_time_ee - start_time_ee:.6f} seconds")

# Some raw attempts at solving the problem using the Extended Euclidean Algorithm and Dynamic Programming
# Keeping this here for reference, but it is not used in the final solution but I do talk about it in the video.

    # # Extended Euclidean
    # start_time_ee = time.time()
    # for machine in machines:
    #     ax, ay, bx, by, prize_x, prize_y = machine
    #     prize_x += 10000000000000  # Adjust prize coordinates for Part 2
    #     prize_y += 10000000000000
    #     cost = solve_machine_part2_extended_euclidean(ax, ay, bx, by, prize_x, prize_y)
    #     if cost != -1:
    #         total_cost_part2_ee += cost
    #         win_count_part2_ee += 1
    # end_time_ee = time.time()
    # elapsed_time_ee = end_time_ee - start_time_ee

    # print("Extended Euclidean Algorithm:")
    # print(f"Fewest tokens to win all possible prizes: {total_cost_part2_ee}")
    # print(f"Number of prizes won: {win_count_part2_ee}")
    # print(f"Elapsed time: {elapsed_time_ee:.6f} seconds")

    # # Dynamic Programming (will likely be very slow or run out of memory)
    # start_time_dp = time.time()
    # for machine in machines:
    #   ax, ay, bx, by, prize_x, prize_y = machine
    #   prize_x += 10000000000000  # Adjust prize coordinates for Part 2
    #   prize_y += 10000000000000
    #   cost = solve_machine_part2_dp(ax, ay, bx, by, prize_x, prize_y)
    #   if cost != -1:
    #       total_cost_part2_dp += cost
    #       win_count_part2_dp += 1
    # end_time_dp = time.time()
    # elapsed_time_dp = end_time_dp - start_time_dp

    # print("\nDynamic Programming (Inefficient):")
    # print(f"Fewest tokens to win all possible prizes: {total_cost_part2_dp}")
    # print(f"Number of prizes won: {win_count_part2_dp}")
    # print(f"Elapsed time: {elapsed_time_dp:.6f} seconds")
    # print("Note: The DP approach is highly inefficient for Part 2 and may take a very long time or run out of memory.")
    
# def extended_euclidean(a, b):
#     """
#     Implements the Extended Euclidean Algorithm.

#     Args:
#         a: The first integer.
#         b: The second integer.

#     Returns:
#         A tuple (gcd, x, y) where gcd is the greatest common divisor of a and b,
#         and x and y are coefficients such that ax + by = gcd.
#     """
#     if a == 0:
#         return (b, 0, 1)
#     else:
#         g, x, y = extended_euclidean(b % a, a)
#         return (g, y - (b // a) * x, x)

# def solve_diophantine(a, b, c):
#     """
#     Solves a linear Diophantine equation of the form ax + by = c.

#     Args:
#         a: The coefficient of x.
#         b: The coefficient of y.
#         c: The constant term.

#     Returns:
#         A tuple (x0, y0, gcd) representing a particular solution (x0, y0) and the
#         greatest common divisor (gcd) of a and b. If no solution exists, returns None.
#     """
#     g, x, y = extended_euclidean(a, b)
#     if c % g != 0:
#         return None  # No solution exists
#     else:
#         x0 = x * (c // g)
#         y0 = y * (c // g)
#         return (x0, y0, g)

# def solve_machine_part2_extended_euclidean(ax, ay, bx, by, prize_x, prize_y):
#     """
#     Solves the claw machine problem for Part 2 using the Extended Euclidean Algorithm.

#     Args:
#         ax: Change in X-coordinate when pressing button A.
#         ay: Change in Y-coordinate when pressing button A.
#         bx: Change in X-coordinate when pressing button B.
#         by: Change in Y-coordinate when pressing button B.
#         prize_x: X-coordinate of the prize (large value).
#         prize_y: Y-coordinate of the prize (large value).

#     Returns:
#         The minimum cost to win the prize, or -1 if no solution exists.
#     """

#     print(f"Solving for machine with: ax={ax}, ay={ay}, bx={bx}, by={by}, prize_x={prize_x}, prize_y={prize_y}")

#     # Solve for x-axis
#     print("  Solving for x-axis...")
#     solution_x = solve_diophantine(ax, bx, prize_x)
#     if solution_x is None:
#         print("  No solution for x-axis.")
#         return -1
#     print("  Solution for x-axis found.")

#     # Solve for y-axis
#     print("  Solving for y-axis...")
#     solution_y = solve_diophantine(ay, by, prize_y)
#     if solution_y is None:
#         print("  No solution for y-axis.")
#         return -1
#     print("  Solution for y-axis found.")

#     a0, b0, gcd_x = solution_x
#     a1, b1, gcd_y = solution_y

#     # Check for compatibility
#     print("  Checking for compatibility...")
#     compatibility_solution = solve_diophantine(bx // gcd_x, -by // gcd_y, a1 - a0)
#     if compatibility_solution is None:
#         print("  Solutions are not compatible.")
#         return -1
#     print("  Solutions are compatible.")

#     t0, _, compatibility_gcd = compatibility_solution

#     # Find the value of k that minimizes 3a + b
#     print("  Finding optimal k...")

#     k_min = - (a0 + (bx / gcd_x) * t0) / ((bx / gcd_x) * (by / gcd_y) / compatibility_gcd)
#     k_max = (b0 - (ax / gcd_x) * t0) / ((ax / gcd_x) * (by / gcd_y) / compatibility_gcd)

#     min_cost = float('inf')
#     for k in range(int(k_min) - 1, int(k_max) + 2):
#         t = t0 + k * (by // gcd_y) // compatibility_gcd
#         a = a0 + (bx // gcd_x) * t
#         b = b0 - (ax // gcd_x) * t

#         if a >= 0 and b >= 0:
#             cost = 3 * a + b
#             if cost < min_cost:
#                 min_cost = cost
#                 print(f"    Found a better solution: a={a}, b={b}, cost={cost}, k={k}")

#     if min_cost == float('inf'):
#         print("  No solution found that satisfies a >= 0 and b >= 0.")
#         return -1

#     print(f"  Minimum cost found: {min_cost}")
#     return min_cost if min_cost != float('inf') else -1

# def solve_machine_part2_dp(ax, ay, bx, by, prize_x, prize_y):
#     """
#     Solves the claw machine problem for Part 2 using Dynamic Programming (Inefficient).

#     Args:
#         ax: Change in X-coordinate when pressing button A.
#         ay: Change in Y-coordinate when pressing button A.
#         bx: Change in X-coordinate when pressing button B.
#         by: Change in Y-coordinate when pressing button B.
#         prize_x: X-coordinate of the prize (large value).
#         prize_y: Y-coordinate of the prize (large value).

#     Returns:
#         The minimum cost to win the prize, or -1 if no solution exists.
#     """
#     # This approach is highly inefficient for large prize coordinates and is not recommended.
#     # It is included here for demonstration purposes only.

#     # The following bounds are just placeholders and will likely be incorrect for large inputs.
#     # You would need a more sophisticated way to estimate appropriate bounds, which is difficult.
    
#     max_a_estimate = prize_x // ax if ax > 0 else prize_x
#     max_b_estimate = prize_y // by if by > 0 else prize_y

#     max_x = min(prize_x, max_a_estimate * ax + max_b_estimate * bx)
#     max_y = min(prize_y, max_a_estimate * ay + max_b_estimate * by)

#     dp = {}
#     dp[(0, 0)] = 0

#     for x in range(int(max_x + 1)):
#         for y in range(int(max_y + 1)):
#             if (x, y) not in dp:
#                 dp[(x, y)] = float("inf")
#             if x >= ax and y >= ay and (x - ax, y - ay) in dp:
#                 dp[(x, y)] = min(dp[(x, y)], dp[(x - ax, y - ay)] + 3)
#             if x >= bx and y >= by and (x - bx, y - by) in dp:
#                 dp[(x, y)] = min(dp[(x, y)], dp[(x - bx, y - by)] + 1)

#     if (prize_x, prize_y) in dp and dp[(prize_x, prize_y)] != float("inf"):
#         return dp[(prize_x, prize_y)]
#     else:
#         return -1