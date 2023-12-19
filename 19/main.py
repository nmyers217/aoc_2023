import re
from copy import deepcopy

def parse_part(s):
    tups = [s2.split('=') for s2 in s[1:-1].split(',')]
    res = {}
    for k,v in tups:
        res[k] = int(v)
    return res

def parse_flow(s):
    res = s
    name, conds = re.search(r"(.+)\{(.+)\}", s).groups()
    conds2 = []
    for c in conds.split(','):
        res = {}
        m = re.search(r"(.+)([<>])(.+):(.+)", c)
        if m:
            src, op, val, to = m.groups()
            res['src'] = src
            res['op'] = op
            res['val'] = int(val)
            res['to'] = to
        else:
            res['to'] = c
        conds2.append(res)
    return name, conds2

def parse_input():
    input = open('./input.txt').read()
    flows,parts = [s.splitlines() for s in input.strip().split('\n\n')]
    parts = [parse_part(p) for p in parts]
    flows = dict(parse_flow(f) for f in flows)
    return flows, parts

flows, parts = parse_input()

A = []
for p in parts:
    cur = 'in'
    while cur != 'A' and cur != 'R':
        for flow in flows[cur]:
            if 'src' not in flow:
                cur = flow['to']
                break
            if flow['op'] == '>':
                if p[flow['src']] > flow['val']:
                    cur = flow['to']
                    break
            else:
                if p[flow['src']] < flow['val']:
                    cur = flow['to']
                    break
    if cur == 'A':
        A.append(p)
        
print(sum(sum(p.values()) for p in A))

def dfs():
    result = []
    ranges = {'x': set(range(1, 4001)),
              'm': set(range(1, 4001)),
              'a': set(range(1, 4001)),
              's': set(range(1, 4001))}

    def helper(node, path=[], ranges=ranges):
        if node == 'A':
            prod = 1
            for v in ranges.values():
                prod *= len(v)
            result.append(prod)
            return 

        if node not in flows:
            return

        for i in range(len(flows[node])):
            ranges2 = deepcopy(ranges)
            f = flows[node][i]

            # We have to do the opposite of the earlier steps we want to avoid
            for j in range(0, i):
                if i == j:
                    continue
                f2 = flows[node][j]
                if f2['op'] == '<':
                    ranges2[f2['src']] = ranges2[f2['src']] & set(range(f2['val'], 4001))
                else:
                    ranges2[f2['src']] = ranges2[f2['src']] & set(range(1, f2['val']+1))

            # Before we can do the actual thing we want to do
            if 'src' in f:
                if f['op'] == '<':
                    ranges2[f['src']] = ranges2[f['src']] & set(range(1, f['val']))
                else:
                    ranges2[f['src']] = ranges2[f['src']] & set(range(f['val']+1, 4001))

            helper(f['to'], path=[*path, f['to']], ranges=ranges2)

    helper('in')
    return result

print(sum(dfs()))

