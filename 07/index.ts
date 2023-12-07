const input = await Deno.readTextFile('./input.txt');
const lines = input.trim().split('\n');

const hands = lines.map(s => s.split(' ')).map(arr => {
  arr[1] = parseInt(arr[1]);
  return arr;
});

const countHand = (hand: string): Record<string, number> => {
  const res: Record<string, number> = {};
  for (const c of hand) {
    res[c] = (res[c] ?? 0) + 1;
  }
  return res;
};

const cardScores: Record<string, number> = {
  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
  'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

const handType = (hand: string, jokered = false) => {
  if (jokered) {
    let best = 0;
    for (const c of Object.keys(cardScores)) {
      const newHand = hand.replaceAll('J', c)
      best = Math.max(best, handType(newHand));
    }
    return best;
  }

  const counts = countHand(hand);
  const [_, values] = [Object.keys(counts), Object.values(counts)];

  const vals: Record<string, number> = {};
  for (const v of values) {
    vals[`${v}`] = (vals[`${v}`] ?? 0) + 1;
  }

  if (values.length === 5) {
    return 0;
  } else if (values.length === 4 && vals['2'] === 1 && vals['1'] === 3) {
    return 1;
  } else if (values.length === 3 && vals['2'] === 2 && vals['1'] === 1) {
    return 2;
  } else if (values.length === 3 && vals['3'] === 1 && vals['1'] === 2) {
    return 3;
  } else if (values.length === 2 && vals['3'] === 1 && vals['2'] === 1) {
    return 4;
  } else if (values.length === 2 && vals['4'] === 1 && vals['1'] === 1) {
    return 5;
  } else if (values.length === 1 && vals['5'] === 1) {
    return 6;
  } else {
    throw new Error(`Could not get type for hand ${hand}`);
  }
};

const compare = (jokered = false) => (a, b) => {
  const [handA] = a;
  const [handB] = b;
  const [typeA, typeB] = [handType(handA, jokered), handType(handB, jokered)];

  if (handA === handB) return 0;

  if (typeA === typeB) {
    for (let i = 0; i < handA.length; i++) {
      if (handA[i] === handB[i]) continue;
      return (cardScores[handA[i]] ?? 0) < (cardScores[handB[i]] ?? 0) ? -1 : 1;
    } 
    return 0;
  } else {
    return typeA - typeB;
  }
};

const sorted = hands.slice(0).sort(compare());
cardScores['J'] = 0;
const jokered = hands.slice(0).sort(compare(true));

let [partOne, partTwo] = [0, 0];
for (let i = 0; i < sorted.length; i++) {
  partOne += (i + 1) * sorted[i][1];
  partTwo += (i + 1) * jokered[i][1];
}

console.log(partOne);
console.log(partTwo);

