const input = await Deno.readTextFile('./input.txt');

const lines = input.split('\n').filter(l => !!l);

function isPossible(set: string): boolean {
  for (const pair of set.split(', ')) {
    const amounts: Record<string, number> = { red: 12, green: 13, blue: 14 }
    const [amt, color] = (pair.trim().match(/(\d+) (.+)/) ?? []).slice(1);
    amounts[color] -= parseInt(amt);
    if (amounts[color] < 0)  return false;
  }
  return true;
}

let partOne = 0;
for (const line of lines) {
  const [id, sets] = (line.match(/Game (\d+): (.+)/) ?? []).slice(1);

  let valid = true;
  for (const s of sets.split(';')) {
    if (!isPossible(s)) valid = false;
  }

  if (valid) partOne += parseInt(id);
}

console.log(partOne);

let partTwo = 0;
for (const line of lines) {
  const [_, sets] = (line.match(/Game (\d+): (.+)/) ?? []).slice(1);

  const maxes: Record<string, number> = { red: 0, green: 0, blue: 0 }
  for (const set of sets.split(';')) {
    for (const pair of set.split(', ')) {
      const [amt, color] = (pair.trim().match(/(\d+) (.+)/) ?? []).slice(1);
      maxes[color] = Math.max(maxes[color], parseInt(amt));
    }
  }

  partTwo += Object.values(maxes).reduce((a, b) => a * b, 1);
}

console.log(partTwo);
