import networkx as nx

DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

with open("day_16/input.txt", "r") as infile:
    data = infile.read().splitlines()
    G = nx.DiGraph()
    start = (139, 1, 3)
    end = (1, 139, 3)

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell != '#':
                for z in range(4):
                    G.add_node((i, j, z))

    for a, b, z in list(G.nodes):
        i, j = DIRECTIONS[z]
        m, n = a + i, b + j
        if (m, n, z) in G.nodes:
            G.add_edge((a, b, z), (m, n, z), weight=1)
        for i in range(4):
            G.add_edge((a, b, z), (a, b, i), weight=1000)

    p1 = nx.shortest_path_length(G, start, end, weight='weight')
    print(p1)
    seats = set()
    for path in nx.all_shortest_paths(G, start, end, weight='weight'):
        for n in path:
            seats.add((n[0], n[1]))
    print(len(seats))