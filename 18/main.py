def parse_input():
    input = open('./input.txt').read()
    lines = [l.split(' ') for l in input.strip().splitlines()]
    return lines

plan = parse_input()
dirs = { 'R': (1,0), 'D': (0,1), 'L': (-1,0), 'U': (0,-1)}

def solve(p2=False):
    loc = (0,0)
    verts = [loc]
    total_len = 0

    for d,n,color in plan:
        n = int(n)
        (dx,dy) = dirs[d]

        if p2:
            l,r = color[2:7], color[7]
            n = int(l, 16)
            (dx,dy) = list(dirs.values())[int(r)]

        next = (loc[0] + n*dx, loc[1] + n*dy)
        total_len += abs(next[0] - loc[0]) + abs(next[1] - loc[1])
        loc = next
        verts.append(loc)

    # Shoelace theorem
    V,l,r = len(verts),0,0
    for i in range(V):
        j = (i+1) % V
        l += verts[i][0] * verts[j][1]
        r += verts[i][1] * verts[j][0]
    shoelace = abs(l-r) // 2

    return shoelace + (total_len // 2) + 1

print(solve())
print(solve(p2=True))

