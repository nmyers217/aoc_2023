def parse_input():
    input = open('./input.txt').read()
    return input.strip().split(',')

def hash(str):
    cur = 0
    for c in str:
        cur += ord(c)
        cur = cur * 17 % 256
    return cur

def init(data):
    boxes = [{} for _ in range(256)]
    for s in data:
        if s.endswith('-'):
            label = s.split('-')[0]
            boxes[hash(label)].pop(label, None)
        else:
            label, n = s.split('=')
            boxes[hash(label)][label] = int(n)
    total = 0
    for i, box in enumerate(boxes):
        for j, (k, v) in enumerate(box.items()):
            total += (i+1) * (j+1) * v
    return total

data = parse_input()

print(sum(hash(s) for s in data))
print(init(data))
