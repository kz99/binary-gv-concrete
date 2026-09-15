# Limited-independence seed-selection gap

## Classification

**Non-explicit existence result; not leaderboard eligible.**

Source: `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-06.json`.

## Result retained

An optimized 4096-wise-independent polynomial family supports an averaging
calculation that would yield a binary code

\[
[2^{30},2955,\ge535{,}822{,}337]_2
\]

after adjoining the all-one word. This reaches the project’s concrete GV
reference in dimension, but it is only an averaging witness: no seed is chosen
by a deterministic polynomial-time algorithm.

Exhaustively fixing seed bits through conditional expectations would reproduce
the same non-explicit defect as the dimension-2971 construction. The source
correctly leaves this as a seed-selection target rather than a code submission.

## Useful conclusions from the audit

- Independent-offset root-killing samplers of the form
  \(\operatorname{Tr}(yP(x))+Q(x)\), with at most 64 zero fibers, have a
  finite dimension ceiling of 996 at this target.
- The equal-block \(\mathbb F_{2^{16}}\)-linear outer code with injective
  binary-linear inner maps is capped at dimension 1040; this cap is attained by
  the RS–RM construction.
- Exact low-wise independence alone is not enough to control the required long
  parity constraints.

## Productive next step

Find an algebraic or combinatorial seed selector for the specified 4096-wise
family and prove all relevant character bounds without enumerating seeds or
matrix completions. A polynomial-time selector with the existing moment bound
would be a qualitatively new explicit construction near the finite GV point.

## Related obstruction trail

- `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-09.json`
  records the same missing compact seed certificate and fixed-inner ceilings.
- `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-10.json`
  explains why exhaustive conditional averages are not an acceptable repair.
- `research_state/campaign-epsilon-2-10-ultra/submissions/composition-09.json`
  places the seed gap alongside the strongest remaining explicit RS gateways.
