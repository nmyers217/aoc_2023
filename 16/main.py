from collections import defaultdict

def parse_input():
    input = open('./input.txt').read()
    lines = input.strip().splitlines()
    res = defaultdict(lambda: '#')
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            res[x,y] = c
    return res

def bfs(g, x=0, y=0, dx=1, dy=0):
    q = [(x,y,dx,dy)]
    seen = set()
    energized = set()
    
    while q:
        x,y,dx,dy = q.pop()
        if (x,y,dx,dy) in seen or g[x,y] == '#':
            continue
        seen.add((x,y,dx,dy))
        energized.add((x,y))
        c = g[x,y]
        if c == '.' or (c == '|' and dy != 0) or (c == '-' and dx != 0):
            q.append((x+dx,y+dy, dx,dy))
        elif c == '\\' or c == '/':
            dx2 = dy * (1 if c == '\\' else -1)
            dy2 = dx * (1 if c == '\\' else -1)
            q.append((x+dx2,y+dy2, dx2,dy2))
        elif c == '|':
            q.append((x,y-1, 0,-1))
            q.append((x,y+1, 0,1))
        elif c == '-':
            q.append((x-1,y, -1,0))
            q.append((x+1,y, 1,0))

    return len(energized)

g = parse_input()
(w, h), _ = next(reversed(g.items()))

print(bfs(g))

starts = []
starts.extend([(x,0,0,1) for x in range(w+1)])
starts.extend([(x,h-1,0,-1) for x in range(w+1)])
starts.extend([(0,y,1,0) for y in range(h+1)])
starts.extend([(w-1,y,-1,0) for y in range(h+1)])
print(max(bfs(g, *args) for args in starts))

