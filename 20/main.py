from collections import deque
from math import lcm

def parse_input():
    input = open('./input.txt').read()
    lines = [l.split(' -> ') for l in input.strip().splitlines()]
    res = {}
    for name, dests in lines:
        node = {}
        node['edges'] = dests.split(', ')
        if name[0] == '%':
            name = name[1:]
            node['type'] = 'FLIP'
            node['state'] = False
        elif name[0] == '&':
            name = name[1:]
            node['type'] = 'CON'
            node['state'] = {}
        else:
            node['type'] = 'BROADCAST'
        res[name] = node

    for name,node in res.items():
        for edge in node['edges']:
            if edge in res and res[edge]['type'] == 'CON':
                res[edge]['state'][name] = 'low'

    return res

def press_button(g, lows_sent={}):
    q = deque([('button', 'broadcaster', 'low')])
    low, high = 1, 0

    while q:
        prev, name, pulse = q.popleft()

        if name in lows_sent and pulse == 'low':
            lows_sent[name] = True
        if name == 'vz' and pulse == 'low':
            # YEAH WHATEVer, TOO BAD!
            lows_sent[name] = True

        if name not in g:
            continue

        node = g[name]

        if node['type'] == 'BROADCAST':
            for edge in node['edges']:
                low += 1
                q.append((name, edge, 'low'))
        elif node['type'] == 'FLIP':
            if pulse == 'high':
                continue
            node['state'] = not node['state']
            for edge in node['edges']:
                if node['state']:
                    high += 1
                    q.append((name, edge, 'high'))
                else:
                    low += 1
                    q.append((name, edge, 'low'))
        elif node['type'] == 'CON':
            node['state'][prev] = pulse
            all_high = all(p == 'high' for p in node['state'].values())
            p = 'low' if all_high else 'high'
            for edge in node['edges']:
                q.append((name, edge, p))
                if p == 'low':
                    low += 1
                else:
                    high += 1

    return low, high

def simulate(graph, presses=1000, end_early=False):
    low, high = 0, 0

    leads_to_rx = None
    for k,v in graph.items():
        if 'rx' in set(v['edges']):
            leads_to_rx = k

    help_me_god = set()
    for k,v in graph.items():
        if leads_to_rx in set(v['edges']):
            help_me_god.add(k)


    lows_sent = dict((k,False) for k in help_me_god)
    lows_sent_at = dict((k,0) for k in lows_sent.keys())

    for i in range(presses):
        l, h = press_button(graph, lows_sent=lows_sent)
        low += l
        high += h

        for k,v in lows_sent.items():
            if v and lows_sent_at[k] == 0:
                lows_sent_at[k] = i + 1

    if end_early:
        vals = []
        for k,v in lows_sent_at.items():
            vals.append(v)
        print(vals)
        return lcm(*vals)

    return low * high

graph = parse_input()
print(simulate(graph))

graph = parse_input()
print(simulate(graph, presses=10000, end_early=True))
