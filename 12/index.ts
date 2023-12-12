let input = `
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
`;
// input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const rows = [];
const groups = [];

for (const line of lines) {
  const [l, r] = line.split(' ');
  rows.push(l);
  groups.push(r.split(',').map(n => parseInt(n)));
}

const permutations = (s: string): string[] => {
  if (!s) return [''];
  const tail = permutations(s.slice(1));
  if (s[0] === '.' || s[0] === '#') {
    return tail.map(s2 => `${s[0]}${s2}`);
  }
  return [
    ...tail.map(s2 => `.${s2}`),
    ...tail.map(s2 => `#${s2}`),
  ];
};

const isValid = (s: string, groups: number[]): boolean => {
  let [count, i, j] = [0, s.indexOf('#'), 0];

  while (i !== -1) {
    if (j >= groups.length) return false;
    count = 0;
    while (s[i] === '#') {
      count++;
      i++;
    }
    if (count !== groups[j]) return false;
    i = s.indexOf('#', i + 1);
    j++;
  }

  return j === groups.length;
};

let p1 = 0;
for (let i = 0; i < rows.length; i++) {
  for (const perm of permutations(rows[i])) {
    if (isValid(perm, groups[i])) p1 += 1;
  }
}

console.log(p1);

let p2 = 0;
for (let i = 0; i < rows.length; i++) {
  let [row, group] = [rows[i], groups[i]];
  for (let j = 0; j < 4; j++) {
    row += `?${row}`;
    group = [...group, ...group];
  }
  // console.log(row, group)
  for (const perm of permutations(row)) {
    if (isValid(perm, group)) p2 += 1;
  }
}

console.log(p2);
