from collections import defaultdict
from copy import deepcopy

def parse_input():
    input = open('./input.txt').read()
    res = [tuple([int(c) for c in p.split(',')]
                   for p in l.split('~'))
             for l in input.strip().splitlines()]
    return res

def grid(bricks):
    """Populate a sparse grid with the bricks"""
    grid = defaultdict(bool)
    for (ax,ay,az), (bx,by,bz) in bricks:
        for x in range(ax, bx+1):
            for y in range(ay, by+1):
                for z in range(az, bz+1):
                    grid[x,y,z] = True
    return grid

def blocked(g, brick):
    (ax,ay,az), (bx,by,bz) = brick
    for x in range(ax, bx+1):
        for y in range(ay, by+1):
            if g[x,y,az-1]:
                return True
    return False

def drop(bricks):
    moved = len(bricks)
    while moved:
        moved = 0
        g = grid(bricks)
        for i in range(len(bricks)):
            (ax,ay,az), (bx,by,bz) = bricks[i]
            if az == 1:
                continue
            if not blocked(g, bricks[i]):
                bricks[i] = ((ax,ay,az-1), (bx,by,bz-1))
                moved += 1
    return bricks

def tick(prev, el):
    """Consumes `prev` in a topological ordering with some kind of bastardized Kahn's algo"""
    g = deepcopy(prev) # wasted an hour here because i forgot to copy :(
    for k in g:
        g[k] = [x for x in g[k] if x != el]
    moved = set()
    count = 1000
    while count:
        count = 0
        for k in g:
            if k not in moved and len(g[k]) == 0:
                moved.add(k)
                count += 1
        for k in g:
            g[k] = [x for x in g[k] if x not in moved]
    return len(moved)

def chain_reaction(prev, single_supports):
    res = 0
    for el in single_supports:
        res += tick(prev, el)
    return res

def solve(bricks):
    prev = defaultdict(list)
    for i in range(len(bricks)):
        (ax_i,ay_i,az_i), (bx_i,by_i,bz_i) = bricks[i]
        for j in range(len(bricks)):
            if i == j:
                continue
            (ax_j,ay_j,az_j), (bx_j,by_j,bz_j) = bricks[j]
            if az_i != bz_j + 1:
                # We only want bricks that are on the level above
                continue
            if ax_i <= bx_j and bx_i >= ax_j and ay_i <= by_j and by_i >= ay_j:
                # And they need to overlap on their x/y plane
                prev[i].append(j)
    disintegrate = set(prev[l][0] for l in prev if len(prev[l]) == 1)
    p1 = len(bricks) - len(disintegrate)
    return p1, chain_reaction(prev, disintegrate)

bricks = parse_input()
dropped = drop(bricks)
print(solve(dropped))

