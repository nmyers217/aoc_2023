from z3 import * 

def parse_input():
    input = open('./input.txt').read()
    lines = [tuple(list(map(int, s.split(', '))) for s in l.split('@'))
             for l in input.strip().splitlines()]
    return lines

data = parse_input()
MIN = 200000000000000
MAX = 400000000000000

def p1():
    lines = []
    for p,v in data:
        # Remember, y = mx + b -- m is slope, and b is intercept
        (x,y,_) = p
        (dx,dy,_) = v
        m = dy / dx # Slope is rise / run = deltaY / deltaX
        b = y - (m * x)
        lines.append([m, b, x, dx > 0])

    res = 0
    seen = set()
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j or (j,i) in seen:
                continue
            seen.add((i,j))
            m1,b1,x1,dx1 = lines[i]
            m2,b2,x2,dx2 = lines[j]

            if m1 == m2:
                # parallel
                continue
            xintercept = (b2 - b1) / (m1 - m2)
            if (xintercept < x1) if dx1 else (xintercept > x1):
                continue
            if (xintercept < x2) if dx2 else (xintercept > x2):
                continue
            yintercept = (m1 * xintercept) + b1
            if all(MIN <= v <= MAX for v in (xintercept, yintercept)):
                res += 1

    return res

def p2():
    """ Just use z3 to solve this... too bad! """
    inp = data[:3]
    t = IntVector('t', len(inp))
    p, v = [IntVector(f'{name}0', 3) for name in ('p', 'v')]
    s = Solver()
    for i in range(len(inp)):
        pi,vi = inp[i]
        for j in range(3):
            s.add(p[j] + v[j] * t[i] == pi[j] + vi[j] * t[i])
    assert(s.check() == sat)
    m = s.model()
    return sum(m[i].as_long() for i in p)

print(p1())
print(p2())
