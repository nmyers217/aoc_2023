const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');
const nums = lines.map(s => s.split(' ').map(n => parseInt(n)));

const getNext = (num: number[]): number[] => {
  let prev = [...num];
  let cur: number[] = [];
  const lastNums: number[] = [prev.at(-1) ?? 0];
  const firstNums: number[] = [prev[0]];

  while (prev.some(n => n !== 0)) {
    for (let i = 1; i < prev.length; i++) {
      cur.push(prev[i] - prev[i-1]);
    }
    lastNums.push(cur.at(-1) ?? 0);
    firstNums.push(cur[0]);
    [prev, cur] = [cur, []];
  }

  let sum = firstNums.pop() ?? 0;
  while (firstNums.length > 0) {
    const [a, b] = [firstNums.pop() ?? 0, sum];
    sum = a - b;
  }

  return [lastNums.reduce((a, b) => a + b, 0), sum];
};

const [p1, p2] = nums
  .map(arr => getNext(arr))
  .reduce((a, b) => [a[0] + b[0], a[1] + b[1]], [0, 0]);

console.log(p1);
console.log(p2);
