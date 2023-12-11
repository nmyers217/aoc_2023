const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const [m, n] = [lines.length, lines[0].length];
const galaxies: number[][] = [];
const [safeRows, safeCols] = [new Set<number>(), new Set<number>()];

for (let y = 0; y < m; y++) {
  for (let x = 0; x < n; x++) {
    if (lines[y][x] === '#') {
      galaxies.push([x, y]);
      safeRows.add(y);
      safeCols.add(x);
    }
  }
}

const combos: number[][] = [];
const seen = new Set<string>();
for (let i = 0; i < galaxies.length; i++) {
  for (let j = 0; j < galaxies.length; j++) {
    if (i === j) continue;
    const c = [i, j].sort();
    if (seen.has(c.toString())) continue;
    combos.push(c);
    seen.add(c.toString());
  }
}

const solve = (mult: number) => {
  let result = 0;
  for (const [i, j] of combos) {
    const [a, b] = [galaxies[i], galaxies[j]];
    let dist = 0;
    const [minX, maxX] = [Math.min(a[0], b[0]), Math.max(a[0], b[0])];
    const [minY, maxY] = [Math.min(a[1], b[1]), Math.max(a[1], b[1])];
    for (let y = minY; y < maxY; y++) {
      dist += safeRows.has(y) ? 1 : mult;
    }
    for (let x = minX; x < maxX; x++) {
      dist += safeCols.has(x) ? 1 : mult
    }
    result += dist;
  }
  return result;
};

console.log(solve(2));
console.log(solve(1_000_000));
