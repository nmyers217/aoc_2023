const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const directions = lines[0];
const map: Record<string, string[]> = lines.slice(2).map(line => {
  const [_, at, l, r] = line.match(/(\w+) = \((\w+), (\w+)\)/) ?? [];
  return [at, l, r]
}).reduce((map, [at, l, r]) => {
  map[at] = [l, r];
  return map;
}, {});

let [cur, i, steps] = ['AAA', 0, 0];
while (cur !== 'ZZZ') {
  steps++;
  const dir = directions[i % directions.length];
  i++;
  cur = map[cur][dir === 'L' ? 0 : 1];
}

console.log(steps);

const starts = Object.keys(map).filter(k => k.endsWith('A'));
const eachSteps = starts.map(_ => 0);
i = 0;

while (starts.some(k => !k.endsWith('Z'))) {
  const dir = directions[i % directions.length];
  i++;
  for (let j = 0; j < starts.length; j++) {
    if (starts[j].endsWith('Z')) continue;
    eachSteps[j]++;
    starts[j] = map[starts[j]][dir === 'L' ? 0 : 1];
  }
}

const lcm = (a: number, b: number) => {
  const [large, small] = [Math.max(a, b), Math.min(a, b)];
  for (i = large; ; i += large) {
    if (i % small == 0) return i;
  }
};

const partTwo = eachSteps.reduce((a, b) => lcm(a, b), Math.max(...eachSteps));

console.log(partTwo);

