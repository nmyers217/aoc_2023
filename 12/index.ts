// I couldn't get deno to use a bigger heap size than 128mb for some reason, no matter what v8 flags i gave it
// which was making this impossible, so i abandoned this and switched to python instead

let input = `
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
`;
input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const rows: string[] = [];
const groups = [];

for (const line of lines) {
  const [l, r] = line.split(' ');
  rows.push(l);
  groups.push(r.split(',').map(n => parseInt(n)));
}

const memo: Record<string, number> = {}

const hash = (s: string, nums: number[]): string => {
  return `${s} - ${nums.toString()}`;
};

const validCombos = (
  s: string,
  nums: number[],
): number => {
  const k = hash(s, nums);
  if (memo[k]) return memo[k];

  if (nums.length === 0) {
    if (s.indexOf('#') >= 0) {
      // The #'s haven't been fully consumed and the groups have, invalid
      return 0;
    } else{ 
      return 1;
    }
  }

  // Try to prune branches that have no chance
  let damaged = nums.reduce((a, b) => a+b, 0);
  for (const c of s) {
    if (c === '#') damaged--;
  }
  if (damaged < 0) {
    // Too many damaged already, so just prune
    memo[k] = 0;
    return 0;
  };
  for (const c of s) {
    if (c === '?') damaged--;
  }
  if (damaged > 0) {
    // Not enough unknowns, so just prune
    memo[k] = 0;
    return 0;
  }

  const n = nums[0];
  let sum = 0;

  for (let i = 0; i < s.length; i++) {
    const longEnough = i+n <= s.length;
    const groupNotEmpty = s.slice(i, i+n).split('').every(c => c !== '.');
    const groupCanStart = i === 0 || s[i-1] !== '#';
    const groupCanEnd = i+n === s.length || s[i+n] !== '#';

    if (longEnough && groupNotEmpty && groupCanStart && groupCanEnd) {
      sum += validCombos(s.slice(i+n+1), nums.slice(1));
    }

    if (s[i] === '#') break;
  }

  memo[k] = sum;
  return memo[k];
}

const questions = (s: string): number =>
  s.split('').filter(c => c === '?').length;

const indexes = new Array(rows.length)
  .fill(0)
  .map((_, i) => i)
  .sort((a, b) => questions(rows[a]) - questions(rows[b]));

let p1 = 0;
for (const i of indexes) {
  p1 += validCombos(rows[i], groups[i]);
}
console.log(p1);

let remaining = rows.length //103;
let p2 = 0//685603741556;
for (const i of indexes) {
  let [row, group] = [rows[i], groups[i]];
  for (let j = 0; j < 4; j++) {
    row += `?${rows[i]}`;
    group = [...group, ...groups[i]];
  }
  p2 += validCombos(row, group);
  remaining--;
  console.log(i, p2, remaining);
}
console.log(p2);
