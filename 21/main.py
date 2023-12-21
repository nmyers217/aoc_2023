from collections import defaultdict, deque

def parse_input():
    input = open('./input.txt').read()
    input = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """
    start = (-1,-1)
    res = defaultdict(lambda: ' ')
    for y,l in enumerate(input.strip().splitlines()):
        for x,c in enumerate(l):
            res[x,y] = c
            if c == 'S':
                start = (x,y)
    return start, res

dirs = [[0,-1],[1,0],[0,1],[-1,0]]
cur, G = parse_input()
W, H = [el+1 for el in next(reversed(G.items()))[0]]
STEPS = 50

q = deque([(0,cur)])
seen = set([cur])
prev = {}
reachable = set([cur])

while q:
    if q[0][0] == STEPS:
        break

    step, (x,y) = q.popleft()
    if step % 2 == 0:
        reachable.add((x,y))

    for (dx,dy) in dirs:
        nx,ny = x+dx, y+dy

        if (nx,ny) in seen:
            continue

        seen.add((nx,ny))
        prev[nx,ny] = (x,y)

        c = G[nx%W,ny%H] 
        if c == '.' or c == 'S':
            q.append((step+1, (nx,ny)))
    
frontier = set(t[1] for t in q)

print(len(frontier) + len(reachable))

