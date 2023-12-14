def parse_input():
    input = open('./input.txt').read()
    paragraphs = input.strip().split('\n\n')
    return [p.split('\n') for p in paragraphs]

def rotate(grid):
    res = ['' for col in range(len(grid[0]))]
    for row in grid:
        for x, c in enumerate(row):
            res[x] += c
    return res

def score(grid, smudge=False):
    for y in range(1, len(grid)):
        if is_reflected(grid, y, smudge=smudge):
            return y * 100
    grid = rotate(grid)
    for y in range(1, len(grid)):
        if is_reflected(grid, y, smudge=smudge):
            return y

def is_reflected(grid, y, smudge=False):
    bot, top = grid[:y], grid[y:]
    smudged = not smudge
    for b, t in zip(reversed(bot), top):
        if b != t:
            if not smudge or smudged:
                return False
            mismatches = sum(b[i] != t[i] for i in range(len(b)))
            if mismatches != 1:
                return False
            smudged = True
    return smudged


data = parse_input()

print(sum(score(grid) for grid in data))
print(sum(score(grid, smudge=True) for grid in data))
