from collections import defaultdict

def parse_input():
    input = open('./input.txt').read()
    start = (-1,-1)
    res = defaultdict(lambda: ' ')
    for y,l in enumerate(input.strip().splitlines()):
        for x,c in enumerate(l):
            res[x,y] = c
            if c == 'S':
                start = (x,y)
    return start, res

steps = 26501365
dirs = [(1,0), (-1,0), (0,1), (0,-1)]
start, G = parse_input()
W, H = [el+1 for el in next(reversed(G.items()))[0]]

visited = defaultdict(set)
visited[0].add(start)
prev_len = 0
a = []

for s in range(steps):
    for x,y in visited[s]:
        for dx,dy in dirs:
            nx, ny = x+dx, y+dy
            if G[nx%W, ny%H] in '.S':
                visited[s+1].add((nx, ny))

    if s % W == steps % W:
        print(s, len(visited.get(s)), len(visited.get(s)) - prev_len, s // W)
        prev_len = len(visited.get(s))
        a.append((s, prev_len))

    if len(a) == 3:
        break

# Problems like today make me really sad
terms = ', '.join(f"({w}, {n})" for w,n in a)
query = f"Interpolate {terms}"
print()
print("Paste this into woflram alpha LOL:")
print(query)
print(f"Then solve the polynomial for x={steps}:")
p2 = 122377//17161 + (29436*26501365)//17161 + (15550*26501365**2)//17161 + 1
print()
print(p2)

