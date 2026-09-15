# Binary GV campaign: current research artifacts

This directory contains artifacts from the 20-researcher ultra-reasoning campaign.
Files under `submissions/` are research outputs, not verified leaderboard records.
A construction is published on the dashboard only after two independent verifier
agents accept its proof.

## Best current internal claim

[`submissions/researcher-0009.json`](submissions/researcher-0009.json) is currently
the strongest candidate. It claims a deterministic binary linear code with

\[
n=2^{30}=1{,}073{,}741{,}824,\qquad
d_{\min}\ge 469{,}762{,}048=\frac{7n}{16},
\]

and dimension `k = 3,916,082`, hence rate

\[
R=\frac{k}{n}=0.0036471355706453323,
\]

slightly above the vanilla GS--Hadamard template ceiling `7/1920`.

The JSON contains the complete construction description, parameter ledger,
distance audit, proof roadmap, and literature dependencies. Its status remains
**under review**; no verifier acceptance has been recorded yet.
