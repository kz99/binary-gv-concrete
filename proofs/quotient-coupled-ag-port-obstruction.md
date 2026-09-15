# Finite obstruction to porting the fixed \(\mathbb F_{256}\) quotient-coupled AG construction

## Scope

This note concerns precisely Construction 4.1 and Theorem 4.2 of the supplied
*Quotient-Coupled Algebraic-Geometry Codes at Every Block Length*.  That
construction fixes the outer field \(K=\mathbb F_{256}\), uses the binary
inner map \(K\to \operatorname{RM}(1,7)\), and appends its two fixed repair
blocks.  It does **not** rule out other AG, concatenated, or
quotient-coupled constructions.

## Proposition

There are no data satisfying Construction 4.1's hypotheses which make its
Theorem 4.2 distance certificate meet the active target
\[
n=2^{30}=1{,}073{,}741{,}824,
\qquad D=535{,}822{,}336.
\]

More explicitly, there are no smooth geometrically irreducible curves
\(X/\mathbb F_{256}\), integers \(L,a\), and \(L+1\) distinct
\(\mathbb F_{256}\)-rational points for which
\[
a+1-g\geq1,\qquad 128L+16{,}512\leq2^{30},
\qquad 64(L-a)\geq D.
\]

## Proof

Put
\[
q_0=D/64=8{,}372{,}224.
\]
The asserted distance bound requires \(L-a\geq q_0\).  The
Riemann--Roch eligibility condition \(a+1-g\geq1\) requires \(a\geq g\).
Consequently
\[
L\geq q_0+g. \tag{1}
\]

Because the construction chooses \(L+1\) distinct rational points on
\(X/\mathbb F_{256}\), Hasse--Weil gives
\[
L+1\leq\#X(\mathbb F_{256})\leq256+1+2g\sqrt{256}=257+32g.
\]
Thus \(L\leq256+32g\).  Combining this with (1) gives
\[
8{,}372{,}224+g\leq256+32g,
\qquad
g\geq\left\lceil\frac{8{,}372{,}224-256}{31}\right\rceil=270{,}064.
\]
It follows from (1) that
\[
L\geq8{,}372{,}224+270{,}064=8{,}642{,}288. \tag{2}
\]
On the other hand, the exact length condition gives
\[
L\leq\left\lfloor\frac{2^{30}-16{,}512}{128}\right\rfloor
=8{,}388{,}479, \tag{3}
\]
which contradicts (2).  Therefore Construction 4.1 has no admissible
specialization with its displayed distance guarantee at the active target.
\(\square\)

## Independent range check

The source's uniform theorem also has the explicit hypothesis
\(0<\delta<7/15\).  The active relative-distance target is
\[
\delta=511/1024=7/15+497/15{,}360>7/15,
\]
so that theorem cannot be invoked directly.  The finite argument above is
stronger for the proposed baseline: it rules out the paper's fixed
\(\mathbb F_{256}\) two-layer construction even before using its modular-curve
specialization.

## Consequence

No under-review leaderboard record is added from this port.  A future port
would need a materially different outer-field/inner-code scaling or a new
distance argument; merely changing the modular level, divisor, or padding in
the stated construction cannot repair this incompatibility.
