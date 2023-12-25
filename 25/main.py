import networkx as nx
from math import prod

def parse_input():
    input = open('./input.txt').read()
    G = nx.Graph()
    for line in input.splitlines():
        left, right = line.split(":")
        for r in right.split():
            G.add_edge(left.strip(), r.strip())
    return G

G = parse_input()

C = nx.minimum_edge_cut(G)
for c in C:
    G.remove_edge(*c)

print(prod(len(x) for x in nx.connected_components(G)))

