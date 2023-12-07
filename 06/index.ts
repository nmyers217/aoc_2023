const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');
const times = (lines[0].match(/\d+/g) ?? []).map(s => parseInt(s));
const distances = (lines[1].match(/\d+/g) ?? []).map(s => parseInt(s));

const partOne = [];

for (let i = 0; i < times.length; i++) {
  const [time, dist] = [times[i], distances[i]];

  let wins = 0;
  for (let charge = 0; charge < time; charge++) {
    const remaining = time - charge;
    const travelled = charge * remaining;
    if (travelled > dist) {
      wins++;
    }
  }
  partOne.push(wins);
}

console.log(partOne.reduce((a, b) => a * b, 1));

const time = parseInt(times.join(''));
const distance = parseInt(distances.join(''));

let wins = 0;
for (let charge = 0; charge < time; charge++) {
  const remaining = time - charge;
  const travelled = charge * remaining;
  if (travelled > distance) {
    wins++;
  }
}

console.log(wins);

