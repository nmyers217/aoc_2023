from z3 import * 

def parse_input():
    input = open('./input.txt').read()
    lines = [tuple(list(map(int, s.split(', '))) for s in l.split('@'))
             for l in input.strip().splitlines()]
    return lines

data = parse_input()
MIN = 200000000000000
MAX = 400000000000000

def ray_intersect(ray_a, ray_b):
    """
    Parametric solution to ray intersection

    A ray is some point P and a vec V, where V can be scaled b U to represent any point on the ray

    Two rays A and B intersect where a solution can be found in the following system of equations:
    
    A + Va*u = B + Vb*v
    """
    # point 1, vec 1, point 2, vec 2
    (p1,v1), (p2,v2) = ray_a, ray_b
    # A and Delta A vecs
    (ax,ay), (adx,ady) = p1[:2], v1[:2]
    # B and Delta B vecs
    (bx,by), (bdx,bdy) = p2[:2], v2[:2]

    # Delta from b-a
    dx,dy = bx-ax, by-ay

    # Determinant
    det = bdx*ady - bdy*adx

    if det == 0:
        # The rays are parallel
        return None

    # U and V scalars to determine point of intersection
    u = (dy*bdx - dx*bdy) / det
    v = (dy*adx - dx*ady) / det

    if u <= 0 or v <= 0:
        # Means intersection is behind ray (in the past)
        return None

    # Intersection locations (equal within epsilon due to floating point precision)
    ix, iy = ax + adx*u, ay + ady*u

    return ix, iy

def p1():
    res = 0
    seen = set()
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j or (j,i) in seen:
                continue
            seen.add((i,j))
            loc = ray_intersect(data[i], data[j])
            if loc is None:
                continue
            if all(MIN <= v <= MAX for v in loc):
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
