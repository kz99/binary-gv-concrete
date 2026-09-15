# Non-explicit constructions

This directory preserves mathematically useful campaign results that fail the
leaderboard's explicitness requirement. A ranked construction must come with a
deterministic algorithm that outputs its complete \(k\times n\) generator
matrix in time \(n^{O(1)}\), together with a proof of that runtime.

The material here is **not** a leaderboard entry, and it must not be described
as an explicit code construction. It is retained because it can expose sharp
finite thresholds, identify the missing derandomization lemma, or supply
reusable Fourier, moment, and expurgation arguments.

## Sweep coverage

On 2026-09-15, the 30 parseable submissions in
`research_state/campaign-epsilon-2-10-ultra/submissions/` were checked against
the polynomial-time full-generator-matrix standard. The two actual
non-explicit constructions and the associated nonconstructive seed result are
indexed below.

| Archive note | Claimed finite result | Why it is not explicit | What remains useful |
| --- | --- | --- | --- |
| [Conditional-average dimension 2971](conditional-average-k2971.md) | A canonical \([2^{30},2971,\ge 535{,}822{,}336]_2\) code | Each matrix bit is selected by an exact average over all remaining completions. | Sharp tail, Fourier, odd-circuit, and hyperplane-expurgation estimates. |
| [Limited-independence seed gap](limited-independence-seed-gap.md) | A 4096-wise family has an averaging witness at dimension 2955. | No polynomial-time deterministic seed selector is given. | A concrete seed-selection target and several architecture ceilings. |

All other candidate constructions in that sweep were structured algebraic or
combinatorial encoders, or were obstruction notes rather than constructions.
They still need their own full-generator runtime certificate before becoming
rankable under the current rule.

## Archive policy

Use these notes to search for a compact seed, a pessimistic estimator with
polynomial-time evaluation, or an algebraic replacement for the nonconstructive
step. Moving such a result to the leaderboard requires a new proof note that
supplies the missing output algorithm and proves its \(n^{O(1)}\) runtime.
