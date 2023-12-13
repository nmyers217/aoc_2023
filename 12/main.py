from functools import cache

def parse_input():
    input = open('./input.txt').read()
    split = [line.split() for line in input.splitlines()]
    parsed = [(a, tuple(int(n) for n in b.split(','))) for a,b in split]
    return parsed

def p1(data):
    return sum(cache_perms(line, counts) for line, counts in data)

def p2(data):
    data = [('?'.join(line for _ in range(5)), counts*5) for line,counts in data]
    return p1(data)

@cache
def cache_perms(line, counts):
    return sum(perms(line, counts))

def perms(line, counts):
    if len(counts) == 0: yield '#' not in line
    else:
        count = counts[0]
        possibles = ((line[:i], line[i:i+count], line[i+count:]) for i in range(len(line) - count + 1))
        for prefix, removed, suffix in possibles:
            if '#' in prefix: break
            if '.' in removed: continue
            if (len(suffix) == 0 or suffix[0] != '#') and (len(prefix) == 0 or prefix[-1] != '#'):
                yield cache_perms(suffix[1:], counts[1:])

data = parse_input()
print(p1(data))
print(p2(data))

