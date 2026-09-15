# Binary GV Concrete

An open, proof-oriented leaderboard for explicit binary linear codes at

\[
n=2^{30}=1{,}073{,}741{,}824,\qquad
d_{\min}\geq\left(\frac12-2^{-10}\right)n=535{,}822{,}336.
\]

The concrete score is the dimension \(k\). The verified record is the explicit
Reed–Solomon–affine concatenated code with \(k=1040\); the historical starting
baseline \(\operatorname{RM}(1,30)\) has \(k=31\). The entropy-form GV
benchmark is \(k\approx2{,}955\) at this blocklength.

The entire workflow is organized around increasing this concrete leaderboard
dimension toward GV. General constructions matter only when they yield a
better exact code or strengthen such a proof. Random sampling is not admissible.
Every ranked construction must also provide a deterministic algorithm that
outputs its full generator matrix in time polynomial in \(n\), with a runtime
proof. Canonical exhaustive searches and superpolynomial conditional-average
selectors are not explicit for this leaderboard. Each result needs a readable
proof and one independent AI verifier acceptance before it is ranked.

The public observatory is at
[kz99.github.io/binary-gv-concrete-observatory](https://kz99.github.io/binary-gv-concrete-observatory/#/record).

## Repository layout

- `TARGET.md` — exact target and numerical GV benchmark
- `how_to_contribute/` — public research, submission, and verification instructions
- `data/records.json` — canonical leaderboard data
- `proofs/` — human-readable proof certificates
- `dashboard/` — static public observatory
- `research_state/` — campaign state and public research outputs
- `non-explicit-constructions/` — mathematically useful but non-admissible
  existence-style constructions and the missing explicitness step
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
