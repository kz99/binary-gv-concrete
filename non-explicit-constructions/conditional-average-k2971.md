# Canonical conditional-average code at dimension 2971

## Classification

**Non-explicit; not leaderboard eligible.**

The two source submissions
`research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-01.json`
and `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-02.json`
give two versions of the same method-of-conditional-probabilities argument. A
legacy reviewer accepted the mathematics before the polynomial-time generator
standard was adopted. That acceptance does not certify explicitness under the
current standard.

## Claimed finite theorem

For

\[
n=2^{30},\qquad D=2^{29}-2^{20}=535{,}822{,}336,
\]

the method canonically defines a binary linear code with parameters

\[
[2^{30},2971,\ge D]_2.
\]

Its claimed rate is \(2971/2^{30}\), slightly above the entropy-form GV
reference used by this project. This is a finite existence-style result, not an
explicit construction in the coding-theory sense used here.

## Construction mechanism

Set \(K=2971\), \(R=D-1\), and let \(G\) range over binary \(K\times n\)
matrices. Define the bad message set

\[
B(G)=\{u\ne0:\operatorname{wt}(uG)\le R\ \text{or}\
\operatorname{wt}(uG)\ge n-R\}.
\]

For odd \(s\), let \(T_s(G)\) count odd circuits lying in \(B(G)\), and put

\[
\Psi(G)=\frac{|B(G)|}{1084}+\sum_{3\le s\le1083\atop s\text{ odd}}T_s(G).
\]

The source proof shows \(\mathbb E\Psi(G)<1\) for a uniformly random matrix.
It then fixes the entries of \(G\) one at a time, choosing the child prefix
with smaller **exact conditional average** of \(\Psi\). The resulting matrix
has \(|B(G)|\le1083\) and no bad odd circuit. Therefore a linear functional
\(\ell\) exists with \(\ell(b)=1\) for all \(b\in B(G)\). On
\(U=\ker\ell\), every nonzero word has weight in \([D,n-D]\); adjoining the
all-one word yields the claimed 2971-dimensional code.

## Why this fails the explicitness requirement

The selector for a single entry of \(G\) asks for the exact average of
\(\Psi\) over every completion of a prefix. There are exponentially many such
completions, and the sources give neither a compact evaluator nor a
polynomial-time pessimistic estimator. Thus the construction is a canonical
exhaustive derandomization, not an \(n^{O(1)}\)-time matrix generator.

The matrix has \(Kn=3{,}190{,}086{,}959{,}104\) entries. Merely writing these
bits is polynomial in \(n\); the obstacle is deciding them by evaluating the
completion averages, which is superpolynomial under the presented method.

## Reusable content

- The exact binomial-tail estimate gives \(2^{2972}p<1083\) at the fixed
  near-half-distance threshold.
- The endpoint Fourier estimate bounds every nontrivial bad-tail coefficient
  by a factor below \(1/256\) of the tail mass.
- The odd-circuit potential and hyperplane-expurgation lemma convert a small,
  circuit-free bad set into a codimension-one balanced subcode.
- The second source proves a scoped barrier at \(K=2972\): the tested
  unconditioned size-plus-circuit potentials and natural exponential tilts have
  expectation at least one. This is not a code upper bound.

## Productive next step

Replace the all-completions average by a polynomial-time computable pessimistic
estimator, a compact algebraic seed certificate, or an explicit small-bias/
expander construction proving the same circuit-free bad-set condition. Only
then can the dimension-2971 argument become a rankable construction.

## Primary sources

- `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-01.json`
- `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-02.json`
- `research_state/campaign-epsilon-2-10-ultra/reviews/combinatorial-01/verifier-1-combinatorial-01.json`
- `research_state/campaign-epsilon-2-10-ultra/submissions/combinatorial-10.json`
