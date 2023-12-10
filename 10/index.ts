// NOTE: I really really should have used some kind of grid helper today

const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const findStart = (): number[] => {
  for (let y = 0; y < lines.length; y++) {
    const line = lines[y];
    for (let x = 0; x < line.length; x++) {
      const c = line[x];
      if (c === 'S') return [x, y];
    }
  }
  throw new Error('no start');
};

const dirToVec: Record<string, number[]> =
  { 'w': [-1,0], 'n': [0,-1], 'e': [1,0], 's': [0,1] };
const vecToDir: Record<string, string> =
  { '-1,0': 'w', '0,-1': 'n', '1,0': 'e', '0,1': 's' }

const flipDir = (dir: string) => {
  return vecToDir[dirToVec[dir].map(el => el * -1).toString()];
}

const pipeInto: Record<string, string[]> = {
  '|': ['n', 's'],
  '-': ['e', 'w'],
  'L': ['s', 'w'],
  'J': ['s', 'e'],
  '7': ['n', 'e'],
  'F': ['n', 'w'],
  '.': [],
}

const pipeFrom: Record<string, string[]> = {
  '|': ['n', 's'],
  '-': ['e', 'w'],
  'L': ['n', 'e'],
  'J': ['n', 'w'],
  '7': ['s', 'w'],
  'F': ['s', 'e'],
  '.': [],
  'S': Object.keys(dirToVec),
}

let dir: string | null = null;
const stack: number[][] = [findStart()];
const seen: Record<string, boolean> = {
  [stack[0].toString()]: true
};

const traverse = () => {
  while (stack.length > 0) {
    const [x, y] = stack[stack.length - 1];
    const sym = lines[y][x];
    const vecs = pipeFrom[sym].map(d => dirToVec[d]);

    let deadEnd = true;
    for (const [dx, dy] of vecs) {
      const [nx, ny] = [x + dx, y + dy];
      if (ny < 0 || ny >= lines.length || nx < 0 || nx >= lines[0].length) continue;

      if (seen[[nx, ny].toString()]) continue;
      const toSym = lines[ny][nx];
      if (toSym === 'S') return stack;

      if (sym === 'S') {
        dir = vecToDir[[dx, dy].toString()];
      }

      if (pipeInto[toSym].includes(dir!)) {
        stack.push([nx, ny]);
        seen[[nx, ny].toString()] = true;
        deadEnd = false;
        dir = flipDir(pipeInto[toSym].filter(d => d !== dir).shift()!);
        break;
      }
    }

    if (deadEnd) {
      return stack
    }
  }
};

const path = traverse()!;
console.log(Math.floor(path.length / 2));

const zoomed: number[][] = new Array(lines.length * 3)
  .fill(0)
  .map(_ => new Array(lines[1].length * 3).fill(0));

for (let y = 0; y < lines.length; y++) {
  const line = lines[y];

  for (let x = 0; x < line.length; x++) {
    const [upX, upY] = [x * 3, y * 3];

    if (seen[[x,y].toString()]) {
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          zoomed[upY + i][upX + j] = 1;
        }
      }
    }
  }
}

const flood = (start: number[], val: number) => {
  const queue = [start];

  while (queue.length > 0) {
    const [x, y] = queue.shift()!;
    if (y < 0 || y >= zoomed.length || x < 0 || x >= zoomed[0].length) continue;

    if (zoomed[y][x] !== 0) continue;
    zoomed[y][x] = val;

    for (const [dx, dy] of Object.values(dirToVec)) {
      const [nx, ny] = [x+dx, y+dy];
      if (ny < 0 || ny >= zoomed.length || nx < 0 || nx >= zoomed[0].length) continue;
      queue.push([nx,ny]);
    }
  }
};

const floodLeftAndRight = (path: number[][]) => {
  for (let i = 1; i < path.length; i++) {
    const [prev, cur] = [path[i-1], path[i]];
    const vec = [cur[0] - prev[0], cur[1] - prev[1]];
    const d = vecToDir[vec.toString()];
    const [x, y] = cur;
    if (d === 'e') {
      flood([x * 3, (y+1) * 3], 2);
      flood([x * 3, (y-1) * 3], 3);
    }
    if (d === 'w') {
      flood([x * 3, (y-1) * 3], 2);
      flood([x * 3, (y+1) * 3], 3);
    }
    if (d === 'n') {
      flood([(x+1) * 3, y * 3], 2);
      flood([(x-1) * 3, y * 3], 3);
    }
    if (d === 's') {
      flood([(x-1) * 3, y * 3], 2);
      flood([(x+1) * 3, y * 3], 3);
    }
  }
};

floodLeftAndRight(path);

// console.log(zoomed.map(row => row.join('')).join('\n'))

// This is an edge case that I didn't notice or handle very well
const surroundedByFourCorners =
  zoomed.flat().filter(el => el === 0).length / 3;

const p2 = Math.min(
  zoomed.flat().filter(el => el === 2).length,
  zoomed.flat().filter(el => el === 3).length
) + surroundedByFourCorners;

console.log(Math.ceil(p2 / (3 * 3)));

