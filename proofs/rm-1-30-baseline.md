# First-order Reed–Muller baseline

## Theorem

There is a deterministic binary linear code with parameters

\[
[2^{30},31,2^{29}]_2.
\]

In particular, it has minimum distance at least

\[
535{,}822{,}336=(1/2-2^{-10})2^{30}.
\]

## Construction

Order the vectors of \(\mathbb F_2^{30}\) lexicographically. For every affine
function

\[
f(x_1,\ldots,x_{30})=a_0+\sum_{i=1}^{30}a_ix_i,
\qquad a_i\in\mathbb F_2,
\]

write its truth table in that order. The set of all such tables is
\(\operatorname{RM}(1,30)\).

## Proof

The affine functions form a 31-dimensional \(\mathbb F_2\)-vector space, and
the constant function together with the 30 coordinate functions are linearly
independent. Evaluation on all points is injective, so the code has dimension
31 and length \(2^{30}\).

Every nonconstant affine function has a nonzero linear part. Translation by a
vector on which that linear part equals one pairs its zeroes with its ones.
Thus it has exactly \(2^{29}\) ones. The nonzero constant function has weight
\(2^{30}\). Hence the minimum distance is exactly \(2^{29}=536{,}870{,}912\),
which exceeds the required distance by \(2^{20}=1{,}048{,}576\). \(\square\)

## Parameter audit

\[
(1/2-2^{-10})2^{30}=2^{29}-2^{20}=535{,}822{,}336.
\]
