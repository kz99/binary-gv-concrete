import katex from 'katex';

const formulas = [
  String.raw`\mathbb{F}_{2}`,
  String.raw`n=2^{30}`,
  String.raw`d_{\mathrm{min}}\geq \frac{7n}{16}`,
  String.raw`R=k/n`,
  String.raw`R>0.0034351348876953125`,
  String.raw`k\ge 3{,}688{,}449`,
  String.raw`d_{\min}\ge469{,}762{,}048`,
];

for (const formula of formulas) {
  katex.renderToString(formula, { throwOnError: true });
}

console.log(`Validated ${formulas.length} dashboard formulas.`);
