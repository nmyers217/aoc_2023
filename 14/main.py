def parse_input():
    input = open('./input.txt').read()
    res = {}
    lines = input.strip().splitlines()
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            res[(x, y)] = c
    return res, len(lines), len(lines[0])

grid, H, W = parse_input()

def move_vert(grid, north=True):
    r = range(H) if north else range(H, -1, -1)
    for y in r:
        for x in range(W):
            if (x,y) in grid and grid[(x,y)] != 'O':
                continue
            y2 = y
            grid[(x,y)] = '.'
            inc = -1 if north else 1
            while (x,y2+inc) in grid and grid[(x,y2+inc)] == '.':
                y2 += inc
            grid[(x,y2)] = 'O'
    return grid

# Too lazy to rotate my sparse grid, too bad!
def move_horiz(grid, west=True):
    r = range(W) if west else range(W, -1, -1)
    for y in range(H):
        for x in r:
            if (x,y) in grid and grid[(x,y)] != 'O':
                continue
            x2 = x
            grid[(x,y)] = '.'
            inc = -1 if west else 1
            while (x2+inc,y) in grid and grid[(x2+inc,y)] == '.':
                x2 += inc
            grid[(x2,y)] = 'O'
    return grid

def calc_load(grid):
    res = 0
    for y in range(H):
        for x in range(W):
            if grid[(x,y)] == 'O':
                res += H - y
    return res

def print_grid(grid):
    for y in range(H):
        str = ''
        for x in range(W):
            str += grid[(x,y)]
        print(str)

def part_two(grid, stop=1_000_000_000):
    g, i = grid, 00
    loads = {}

    while i < stop:
        g = move_vert(g, north=True)
        g = move_horiz(g, west=True)
        g = move_vert(g, north=False)
        g = move_horiz(g, west=False)
        i += 1
        loads[i] = calc_load(g)
        # I hardcoded this after looking at my output, too bad!
        CYCLE_LENGTH = 9
        if i == 1000:
            i += ((stop - i * 2) // CYCLE_LENGTH) * CYCLE_LENGTH

    print(loads[stop])

print(calc_load(move_vert(grid)))
part_two(grid)
