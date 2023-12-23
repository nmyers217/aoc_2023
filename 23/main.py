from collections import defaultdict
from copy import deepcopy

def parse_input():
    input = open('./input.txt').read()
    lines = input.strip().splitlines()
    grid = defaultdict(lambda: '#')
    for y,row in enumerate(lines):
        for x,c in enumerate(row):
            grid[x,y] = c
    W,H = x,y
    return grid, W, H

dirs = [[0,-1],[1,0],[0,1],[-1,0]]
grid, W, H = parse_input()
start = (1,0)
end = (W-1,H)

def to_graph(grid, p2=False):
    node = defaultdict(lambda: {})
    for y in range(H):
        for x in range(W):
            if grid[x,y] == '#':
                continue
            if p2:
                for dx,dy in dirs:
                    if grid[x+dx,y+dy] != '#':
                        node[x,y][x+dx,y+dy] = 1
            else:
                if grid[x,y] == '.':
                    for dx,dy in dirs:
                        if grid[x+dx,y+dy] != '#':
                            node[x,y][x+dx,y+dy] = 1
                elif grid[x,y] == '>':
                    node[x,y][x+1,y] = 1
                elif grid[x,y] == 'v':
                    node[x,y][x,y+1] = 1
                elif grid[x,y] == '<':
                    node[x,y][x-1,y] = 1
                elif grid[x,y] == '^':
                    node[x,y][x,y-1] = 1
    return node

def shrink_to_intersections(graph):
    res = deepcopy(graph)
    keys = list(res.keys())
    for k in keys:
        if len(graph[k]) == 2:
            # not an intersection, so get rid of it
            p,n = res[k].keys()
            dist = res[k][p] + res[k][n]
            if k in res[p]:
                res[p][n] = dist
                del res[p][k]
            if k in res[n]:
                res[n][p] = dist
                del res[n][k]
            del res[k]
    return res

def dfs(graph, start, end, path):
    if start == end:
        return max(path.values())
    longest = 0
    for k in graph[start]:
        if k in path:
            continue
        new = path.copy()
        new[k] = path[start] + graph[start][k]
        longest = max(longest, dfs(graph, k, end, new))
    return longest

grid1 = to_graph(grid)
grid2 = to_graph(grid, p2=True)

print(dfs(shrink_to_intersections(grid1), start, end, {start: 0}))
print(dfs(shrink_to_intersections(grid2), start, end, {start: 0}))


