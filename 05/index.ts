const input = await Deno.readTextFile('./input.txt');

const groups = input.trim().split('\n\n');

const seeds = (groups.at(0)?.match(/\d+/g) ?? []).map(s => parseInt(s));

let curSeeds = seeds.map(el => el);
for (const group of groups.slice(1)) {
  const nums = (group.match(/\d+/g) ?? []).map(s => parseInt(s));

  curSeeds = curSeeds.map(seed => {
    for (let i = 0; i < nums.length; i += 3) {
      const [dest, source, range] = [nums[i], nums[i+1], nums[i+2]];
      if (source <= seed && seed <= source + range) {
        return dest + (seed - source);
      }
    }
    return seed;
  });
}

const partOne = Math.min(...curSeeds);
console.log(partOne);

// Stupid brute force because range splitting is boring and tedious
let partTwo = 0;
const reverseGroups = input.split('\n\n').slice(1).map(
  g => g.split('\n').slice(1).map(x => x.split(' ').map(y => parseInt(y)))
).reverse();
while (++partTwo) {
  let x = partTwo;
  reverseGroups.forEach(g => {
    const r = g.find(r => {
      return r[0] <= x && r[0] + r[2] > x;
    });
    if (!r) return;
    x += r[1] - r[0];
  });
  if (seeds.find((s, i) => !(i % 2) && x >= s && x < s + seeds[i+1])) {
    break;
  }
}
console.log(partTwo);

