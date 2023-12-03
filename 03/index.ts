const input = await Deno.readTextFile('./input.txt');
const lines = input.split('\n').filter(l => !!l);

const nums = new Set<string>(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']);
const neighbors = [
  [-1,-1], [0,-1], [1,-1],
  [-1,0], [1,0],
  [-1,1], [0,1], [1,1]
];
const parts: Record<string, number> = {};
const gears: Record<string, number[]> = {};

const key = (x: any, y: any) => `${x},${y}`;

for (let i = 0; i < lines.length; i++) {
  const row = lines[i];

  for (let j = 0; j < row.length; j++) {
    const char = row[j];

    if (char === '.' || nums.has(char)) continue;

    for (const [dx, dy] of neighbors) {
      const [x, y] = [j + dx, i + dy];

      if (x < 0 || x >= row.length || y < 0 || y >= lines.length) continue;
      const neighbor = lines[y][x];
      if (!nums.has(neighbor)) continue;
      
      let [left, right] = [x, x];
      while (nums.has(lines[y][left - 1])) left--;
      while (nums.has(lines[y][right + 1])) right++;

      const num = parseInt(lines[y].slice(left, right + 1));

      if (parts[key(left, y)] !== undefined) continue;

      parts[key(left, y)] = num;
      if (char === '*') {
        gears[key(i, j)] = [
          ...(gears[key(i, j)] ?? []),
          num,
        ]
      }
    } 
  }
}

const partOne = Object.values(parts).reduce((a, b) => a + b, 0);

const partTwo = Object.values(gears)
  .filter(arr => arr.length === 2)
  .reduce((a, [one, two]) => a + one * two, 0)

console.log(partOne);
console.log(partTwo);

