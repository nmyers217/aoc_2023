const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

let partOne = 0;

const sanitize = (str: string): string[] => str
  .trim()
  .split(' ')
  .map(el => el.trim())
  .filter(el => el !== '');

const tally: Record<string, number> = {};

const inc = (n: number) => {
  if (tally[`${n}`] === undefined) {
    tally[`${n}`] = 0;
  }
  tally[`${n}`]++;
}

for (const l of lines) {
  const [id, winners, present] = (l.match(/Card(.+):(.+)\|(.+)/) ?? []).slice(1);
  const idNum = parseInt(id.trim());
  const s = new Set<string>(sanitize(winners));

  inc(idNum);
  let score = 0;
  let matches = 0;
  for (const p of sanitize(present)) {
    if (s.has(p)) {
      score === 0 ? score++ : score *= 2;
      matches++;
    }
  }

  partOne += score;

  for (let copy = 0; copy < tally[`${idNum}`]; copy++) {
    for (let i = 1; i <= matches; i++) {
      inc(Math.min(idNum + i, lines.length))
    }
  }
}

const partTwo = Object.values(tally).reduce((a, b) => a + b, 0);

console.log(partOne);
console.log(partTwo)
