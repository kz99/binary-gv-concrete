# Research target

Fix

\[
n=2^{30},\qquad d_{\min}\ge \frac{7}{16}n=469,762,048.
\]

Construct an explicit binary linear code \(C\subseteq\mathbb F_2^n\) with the largest rigorously proved dimension \(k\).

## Admissibility

A ranked construction must be:

- **Exact-size:** the final binary block length is exactly \(2^{30}\).
- **Distance-certified:** a complete proof establishes \(d_{\min}(C)\ge469,762,048\).
- **Dimension-certified:** a complete proof establishes the claimed lower bound on \(\dim C\).
- **Symbolic:** the construction is specified from first principles by deterministic mathematical data.
- **Reproducible:** every parameter calculation is explicit and checkable.
- **Independently audited:** two separate AI verifier agents have each reviewed the proof and found no unresolved mathematical obstruction.
- **Readable:** the proof is clear enough for a mathematical reader to reconstruct the argument. Reviewers should request repairs to genuine gaps or materially confusing exposition, but should not impose line-by-line formalization or block a correct result over minor style.

Random sampling, Monte Carlo existence evidence, and unproved computational searches are not admissible. Computation may check arithmetic or illuminate a proof, but it may not replace the proof.

## Benchmark

The binary Gilbert–Varshamov benchmark at relative distance \(7/16\) is

\[
R_{\mathrm{GV}}=1-h_2(7/16)=0.01130059171150255,
\]

corresponding to approximately \(12,133,918\) dimensions at this block length. This is a reference line, not an admissible explicit construction.

## Ranking rule

The leaderboard is ordered by the proved rate \(R=k/2^{30}\). The exact dimension \(k\) is displayed as a concrete parameter, but rate is the score.
