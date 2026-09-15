# Densified Garcia–Stichtenoth plus RM(1,7)

## Theorem

There is an explicit binary linear code with parameters

\[
[2^{30},\,\ge 3,688,448,\,\ge 469,762,048]_2.
\]

## Construction

Let \(q=16\), so the outer alphabet is \(\mathbb F_{q^2}=\mathbb F_{256}\). Use level \((k,s)=(4,3)\) of the densified Garcia–Stichtenoth tower. At this level take the standard set of

\[
L=(q^2-1)q^{k-1}2^s=8,355,840
\]

rational evaluation places, excluding the distinguished rational place \(P_\infty\). The standard genus formula gives

\[
g_5=16^5+16^4-16^3-2\cdot16^2+1=1,109,505,
\]

and the densified-tower bound gives

\[
g_{4,3}\le \left\lfloor \frac{g_5}{2}+1\right\rfloor=554,753.
\]

Set the designed outer distance to

\[
d_{\mathrm{out}}=7,340,032
\]

and take the divisor

\[
G=1,015,808P_\infty,
\qquad
\deg G=L-d_{\mathrm{out}}=1,015,808.
\]

As \(\deg G<L\), evaluation is injective. Riemann–Roch gives

\[
k_{\mathrm{out}}\ge \deg G+1-g_{4,3}=461,056.
\]

Concatenate with the binary Reed–Muller code

\[
\operatorname{RM}(1,7)=[128,8,64]_2,
\]

using an \(\mathbb F_2\)-linear identification \(\mathbb F_{256}\cong\mathbb F_2^8\). Finally append \(4,194,304\) zero coordinates.

## Proof of parameters

Concatenation multiplies the outer length by \(128\), the outer dimension by \(8\), and the outer minimum distance by at least \(64\). Hence, before padding, the binary code has

\[
n'=8,355,840\cdot128=1,069,547,520,
\]

\[
k'\ge461,056\cdot8=3,688,448,
\]

and

\[
d'\ge7,340,032\cdot64=469,762,048.
\]

Appending zero coordinates preserves dimension and minimum distance, while

\[
n'+4,194,304=1,073,741,824=2^{30}.
\]

Therefore the padded code has the claimed parameters. \(\square\)

In particular, its certified rate is

\[
R\ge \frac{3,688,448}{2^{30}}=0.0034351348876953125.
\]

## Verifier audit

- Evaluation injectivity: passed.
- Riemann–Roch dimension arithmetic: passed.
- Inner-code parameters: passed.
- Concatenated length, dimension, and distance: passed.
- Zero-padding step: passed.

## References

- S. Ballet, J. Pieltant, M. Rambaud, and J. Sijsling, *On the tensor rank of multiplication in finite extensions of finite fields and related issues in algebraic geometry*, Proposition 2.1 and the displayed Garcia–Stichtenoth genus formula. [Author-hosted PDF](https://perso.telecom-paristech.fr/rambaud/articles/BPRS.pdf)
- H. Stichtenoth, *Algebraic Function Fields and Codes*, second edition, Springer, 2009, Chapter 2 (Riemann–Roch and algebraic-geometry evaluation codes).
