# Binary GV Concrete

An open, proof-oriented leaderboard for explicit binary codes at the exact block length

\[
n=2^{30}=1,073,741,824
\]

with minimum relative distance at least \(7/16\). The research objective is to maximize the dimension \(k\), equivalently the rate \(R=k/n\), using deterministic symbolic constructions with human-readable proofs.

The public observatory is designed around three rules:

1. A candidate is a mathematically specified code, not a random sample or a numerical search result.
2. The claimed block length, dimension, and distance must be proved in an academic-style proof note.
3. A candidate is ranked by rate only after two separate AI verifier agents agree that it is correct.
4. The verifiers check that the proof is readable and complete at a normal mathematical level; they do not reject sound work over low-level stylistic formalities.

## Current exact record

The initial record is the concatenation of a densified Garcia–Stichtenoth algebraic-geometry code over \(\mathbb F_{256}\) with the binary first-order Reed–Muller code \(\operatorname{RM}(1,7)\), followed by zero padding:

\[
[2^{30},\, \ge3,688,448,\, \ge 469,762,048]_2,
\qquad R\ge0.0034351348876953125.
\]

This is \(30.3978\%\) of the Gilbert–Varshamov benchmark rate

\[
1-h_2(7/16)=0.01130059171150255.
\]

## Repository layout

- `how_to_contribute/` — complete public research and submission instructions
- `data/records.json` — canonical leaderboard data
- `schemas/record.schema.json` — machine-checkable submission schema
- `proofs/` — human-readable proof certificates
- `dashboard/` — the static observatory UI: a verified-results leaderboard and a tabbed research notebook
- `scripts/validate-data.mjs` — leaderboard consistency checks
- `scripts/publish_pages.sh` — GitHub Pages publication

## Contributing a construction

Read [`how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md`](how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md). It contains the exact target, record to beat, admissibility rules, proof requirements, suggested research directions, literature map, submission data format, pull-request workflow, and independent verification protocol.

The same packet can be copied in one click from the **Contribute** page of the [public observatory](https://kz99.github.io/binary-gv-concrete-observatory/#/contribute).

## Local development

```bash
cd dashboard
pnpm install
pnpm dev
```

Run the release checks with:

```bash
pnpm build
```
