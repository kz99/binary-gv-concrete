# Binary GV Concrete

An open, proof-oriented leaderboard for explicit binary linear codes at

\[
n=2^{30}=1{,}073{,}741{,}824,\qquad
d_{\min}\geq\left(\frac12-2^{-10}\right)n=535{,}822{,}336.
\]

The concrete score is the dimension \(k\). The present verified baseline is
\(\operatorname{RM}(1,30)\), with \(k=31\) and distance \(2^{29}\). The
entropy-form GV benchmark is \(k\approx2{,}955\) at this blocklength.

The larger goal is an explicit, symbolic family at relative distance
\(1/2-\varepsilon\) and rate \(\Omega(\varepsilon^2)\). Random sampling is
not an admissible construction method. Each result needs a readable proof, and
two independent AI verifiers must accept it before it is ranked.

The public observatory is at
[kz99.github.io/binary-gv-concrete-observatory](https://kz99.github.io/binary-gv-concrete-observatory/#/record).

## Repository layout

- `TARGET.md` — exact target and numerical GV benchmark
- `how_to_contribute/` — public research, submission, and verification instructions
- `data/records.json` — canonical leaderboard data
- `proofs/` — human-readable proof certificates
- `dashboard/` — static public observatory
- `research_state/` — campaign state and public research outputs
- `archive/target-7-16/` — historical, non-current campaign material

## Contributing

Read [the contributor instructions](how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md).
They state the exact target, proof standard, data format, verifier gate, and
pull-request workflow. The same text is available with one-click copy on the
observatory’s Contribute page.

## Local development

```bash
cd dashboard
pnpm install
pnpm build
```
