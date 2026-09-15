import katex from 'katex';

const formulas = [
  String.raw`\mathbb{F}_{2}`,
  String.raw`n=2^{30}`,
  String.raw`d_{\mathrm{min}}\geq (1/2-2^{-10})n`,
  String.raw`k`,
  String.raw`k\geq 32`,
  String.raw`d_{\mathrm{min}}\geq 535{,}822{,}336`,
  String.raw`k\approx 2{,}955`,
];

for (const formula of formulas) {
  katex.renderToString(formula, { throwOnError: true });
}

console.log(`Validated ${formulas.length} dashboard formulas.`);
