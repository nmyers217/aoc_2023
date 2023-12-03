const input = await Deno.readTextFile('./input.txt');

const lines = input.split('\n').filter(l => !!l);

const partOne = lines
  .map(l => l.match(/\d/g))
  .map(arr => parseInt((arr?.at(0) ?? '') + arr?.at(-1)))
  .reduce((a, b) => a + b, 0);

console.log(partOne)

const numMap: Record<string, string> =
  { one: '1', two: '2', three: '3', four: '4', five: '5', six: '6', seven: '7', eight: '8', nine: '9' };

let partTwo = 0;
for (const l of lines) {
  let value = '';
  const keys = [...Object.keys(numMap), ...Object.values(numMap)];

  let i = 0;
  while (true) {
    let found = false;
    for (const k of keys) {
      if (l.slice(i).startsWith(k)) {
        value += numMap[k] ? numMap[k] : k;
        found = true;
      }
    }
    if (found) break;
    i++;
  }

  let j = l.length - 1;
  while (true) {
    let found = false;
    for (const k of keys) {
      if (l.slice(j).startsWith(k)) {
        value += numMap[k] ? numMap[k] : k;
        found = true;
      }
    }
    if (found) break;
    j--;
  }

  partTwo += parseInt(value);
}

console.log(partTwo)


