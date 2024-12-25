from itertools import combinations
import timeit

def parse_input(input_text):
    """
    Parses the input text to extract network connections and computers.

    Args:
        input_text: The input string containing the network connections.

    Returns:
        A tuple containing:
            - connections: A dictionary representing the network connections.
            - computers: A set of computer names.
    """
    connections = {}
    computers = set()
    for line in input_text.strip().split('\n'):
        comp1, comp2 = line.strip().split('-')
        connections.setdefault(comp1, set()).add(comp2)
        connections.setdefault(comp2, set()).add(comp1)
        computers.add(comp1)
        computers.add(comp2)
    return connections, computers

def solve_part_one_optimized(input_text):
    """
    Finds the number of interconnected trios of computers containing at least one computer
    whose name starts with 't'.

    Args:
        input_text: The input string containing the network connections.

    Returns:
        The number of interconnected trios containing 't'.
    """
    connections, computers = parse_input(input_text)
    t_computers = [comp for comp in computers if comp.startswith('t')]
    interconnected_trios_with_t = set()

    for t_comp in t_computers:
        neighbors = connections.get(t_comp, set())
        for neighbor1, neighbor2 in combinations(neighbors, 2):
            if neighbor2 in connections.get(neighbor1, set()):
                trio = frozenset({t_comp, neighbor1, neighbor2})
                interconnected_trios_with_t.add(trio)

    return len(interconnected_trios_with_t)

def is_clique(nodes, connections):
    """
    Checks if a given set of nodes forms a clique in the network.

    Args:
        nodes: A set of computer names.
        connections: A dictionary representing the network connections.

    Returns:
        True if the nodes form a clique, False otherwise.
    """
    for pair in combinations(nodes, 2):
        comp1, comp2 = pair
        if comp2 not in connections.get(comp1, set()):
            return False
    return True

def solve_part_two_brute_force(input_text):
    """
    Finds the largest fully connected group of computers (maximum clique) using a brute-force approach.

    Args:
        input_text: The input string containing the network connections.

    Returns:
        A set of computer names representing the largest clique.
    """
    connections, computers = parse_input(input_text)
    max_clique = set()
    for i in range(1, len(computers) + 1):
        for subset in combinations(computers, i):
            if is_clique(subset, connections):
                if len(subset) > len(max_clique):
                    max_clique = set(subset)
    return max_clique

def solve_part_two_backtracking(input_text):
    """
    Finds the largest fully connected group of computers (maximum clique) using a backtracking (Bron-Kerbosch) approach.

    Args:
        input_text: The input string containing the network connections.

    Returns:
        A set of computer names representing the largest clique.
    """
    connections, computers = parse_input(input_text)
    adj = {computer: connections.get(computer, set()) for computer in computers}
    max_clique = set()

    def bron_kerbosch(r, p, x):
        nonlocal max_clique
        if not p and not x:
            if len(r) > len(max_clique):
                max_clique = r.copy()
            return

        if p:
            pivot = next(iter(p.union(x)))
            candidates = p.difference(adj[pivot])
            for v in list(candidates):
                bron_kerbosch(r.union({v}), p.intersection(adj[v]), x.intersection(adj[v]))
                p.remove(v)
                x.add(v)

    bron_kerbosch(set(), computers.copy(), set())
    return max_clique

def get_lan_party_password(lan_party_computers):
    """
    Generates the LAN party password from the set of computers.

    Args:
        lan_party_computers: A set of computer names in the LAN party.

    Returns:
        The LAN party password string.
    """
    sorted_computers = sorted(list(lan_party_computers))
    return ",".join(sorted_computers)

def test_solve_part_one_optimized():
    example_input = """
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """
    expected_output = 7
    actual_output = solve_part_one_optimized(example_input)
    assert actual_output == expected_output, f"Part 1 Test failed: expected {expected_output}, got {actual_output}"
    print("Part 1 Test passed!")

def test_solve_part_two():
    example_input = """
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """
    expected_lan_party = {"co", "de", "ka", "ta"}
    expected_password = "co,de,ka,ta"

    # Test Brute Force
    actual_lan_party_brute_force = solve_part_two_brute_force(example_input)
    assert actual_lan_party_brute_force == expected_lan_party, f"Part 2 (Brute Force) Test failed: expected {expected_lan_party}, got {actual_lan_party_brute_force}"
    actual_password_brute_force = get_lan_party_password(actual_lan_party_brute_force)
    assert actual_password_brute_force == expected_password, f"Part 2 (Brute Force) Password Test failed: expected {expected_password}, got {actual_password_brute_force}"
    print("Part 2 (Brute Force) Test passed!")

    # Test Backtracking
    actual_lan_party_backtracking = solve_part_two_backtracking(example_input)
    assert actual_lan_party_backtracking == expected_lan_party, f"Part 2 (Backtracking) Test failed: expected {expected_lan_party}, got {actual_lan_party_backtracking}"
    actual_password_backtracking = get_lan_party_password(actual_lan_party_backtracking)
    assert actual_password_backtracking == expected_password, f"Part 2 (Backtracking) Password Test failed: expected {expected_password}, got {actual_password_backtracking}"
    print("Part 2 (Backtracking) Test passed!")

if __name__ == "__main__":
    test_solve_part_one_optimized()
    test_solve_part_two()

    with open("day_23/input.txt", "r") as file:
        input_data = file.read()

    print("\n--- Benchmarking ---")

    # Benchmark Part 1
    time_part1 = timeit.timeit(lambda: solve_part_one_optimized(input_data), number=10)
    print(f"Part 1 (Optimized) execution time (10 runs): {time_part1:.4f} seconds")

    # Benchmark Part 2 (Brute Force)
    # time_part2_brute_force_example = timeit.timeit(lambda: solve_part_two_brute_force(test_solve_part_two.__code__.co_consts[1]), number=10)
    # print(f"Part 2 (Brute Force) on Example Input execution time (10 runs): {time_part2_brute_force_example:.4f} seconds")
    # time_part2_brute_force_actual = timeit.timeit(lambda: solve_part_two_brute_force(input_data), number=1)
    # print(f"Part 2 (Brute Force) on Actual Input execution time (1 run): {time_part2_brute_force_actual:.4f} seconds")

    # Benchmark Part 2 (Backtracking)
    time_part2_backtracking_example = timeit.timeit(lambda: solve_part_two_backtracking(test_solve_part_two.__code__.co_consts[1]), number=10)
    print(f"Part 2 (Backtracking) on Example Input execution time (10 runs): {time_part2_backtracking_example:.4f} seconds")
    time_part2_backtracking_actual = timeit.timeit(lambda: solve_part_two_backtracking(input_data), number=1)
    print(f"Part 2 (Backtracking) on Actual Input execution time (1 run): {time_part2_backtracking_actual:.4f} seconds")

    print("\n--- Part 2 Solutions ---")
    # lan_party_brute_force = solve_part_two_brute_force(input_data)
    # password_brute_force = get_lan_party_password(lan_party_brute_force)
    # print(f"Part 2 (Brute Force) - LAN Party: {lan_party_brute_force}")
    # print(f"Part 2 (Brute Force) - Password: {password_brute_force}")

    lan_party_backtracking = solve_part_two_backtracking(input_data)
    password_backtracking = get_lan_party_password(lan_party_backtracking)
    print(f"Part 2 (Backtracking) - LAN Party: {lan_party_backtracking}")
    print(f"Part 2 (Backtracking) - Password: {password_backtracking}")