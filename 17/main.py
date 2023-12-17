from collections import defaultdict
import heapq

def parse_input():
    input = open('./input.txt').read()
    lines = input.strip().splitlines()
    result = []
    for line in lines:
        result.append([int(c) for c in line])
    return result

grid = parse_input()
W, H = len(grid[0]), len(grid)

graph = defaultdict(lambda: '#')
for y,row in enumerate(grid):
    for x,n in enumerate(row):
        graph[x,y] = n

def search(graph, dir, ultra=False):
    q = []
    heapq.heappush(q, (0, 0,0, *dir, 0))
    seen = set()
    
    while q:
        loss, x,y, dx,dy, moves = heapq.heappop(q)

        if (x,y) == (W-1,H-1):
            if not ultra or moves >= 4:
                return loss

        if (x,y,dx,dy,moves) in seen:
            continue
        seen.add((x,y,dx,dy,moves))

        dirs = []
        if ultra:
            if moves < 4:
                dirs.append((dx, dy))
            else:
                dirs.extend([(dy, dx*-1), (dy*-1, dx)])
                if moves < 10:
                    dirs.append((dx, dy))
        else:
            if moves < 3:
                dirs.append((dx, dy))
            dirs.extend([(dy, dx*-1), (dy*-1, dx)])

        for dx2,dy2 in dirs:
            x2,y2 = x+dx2, y+dy2
            n = graph[x2,y2]
            if n == '#':
                continue
            moves2 = moves + 1 if (dx,dy) == (dx2,dy2) else 1
            loss2 = loss + n
            heapq.heappush(q, (loss2, x2,y2, dx2,dy2, moves2))

print(search(graph, (1,0)))
print(min(search(graph, (1,0), ultra=True),
          search(graph, (0,1), ultra=True)))

