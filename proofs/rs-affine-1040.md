# An explicit Reed–Solomon–affine code of dimension 1,040

## Theorem

There is a deterministic binary linear code

\[
C\subseteq \mathbb F_2^{2^{30}}
\]

with

\[
\dim C=1040,
\qquad
d_{\min}(C)\ge 535{,}822{,}336
=\left(\frac12-2^{-10}\right)2^{30}.
\]

Its complete generator matrix can be output deterministically in time polynomial
in the block length.

## Construction

Let

\[
p(T)=T^{16}+T^5+T^3+T^2+1\in\mathbb F_2[T].
\]

Repeated squaring modulo \(p\) gives

\[
T^{2^8}\equiv T^8+T^7+T^3+T,
\qquad
T^{2^{16}}\equiv T.
\]

Put \(h=T^8+T^7+T^3\). Direct Euclidean division gives

\[
\begin{aligned}
p&=(T^8+T^7+T^6+T^5+T^4+T^2+1)h+(T^2+1),\\
h&=(T^6+T^5+T^4+T^3+T^2+1)(T^2+1)+1.
\end{aligned}
\]

Hence \(\gcd(p,T^{2^8}-T)=1\). Since the only prime divisor of \(16\)
is \(2\), the Rabin irreducibility criterion shows that \(p\) is
irreducible. Define

\[
F=\mathbb F_2[T]/(p),\qquad \alpha=T\bmod p.
\]

Use the polynomial basis \(1,\alpha,\ldots,\alpha^{15}\), and set

\[
A=\operatorname{span}_{\mathbb F_2}
\{1,\alpha,\ldots,\alpha^{14}\}\subset F,
\qquad |A|=2^{15}.
\]

For \(z=\sum_{i=0}^{15}z_i\alpha^i\in F\) and
\(y=(y_1,\ldots,y_{15})\in\mathbb F_2^{15}\), define

\[
H(z)_y=z_0+\sum_{i=1}^{15}z_i y_i.
\]

Finally, let \(M=F[X]_{\le 64}\) and define

\[
\operatorname{Enc}(f)=\bigl(H(f(a))_y\bigr)_{(a,y)\in
A\times\mathbb F_2^{15}}.
\]

All bases and coordinates are ordered lexicographically by their binary
coefficient vectors. The code is \(C=\operatorname{Enc}(M)\).

## Proof of length and dimension

The map \(H:F\to\mathbb F_2^{2^{15}}\) is binary linear and injective: its
coordinates at \(y=0,e_1,\ldots,e_{15}\) recover all sixteen coefficients of
\(z\). Evaluation on \(A\) is also binary linear.

If \(f\in M\) vanishes at every point of \(A\), then either \(f=0\), or a
nonzero polynomial of degree at most \(64\) has \(2^{15}\) roots. The latter is
impossible. Thus \(\operatorname{Enc}\) is injective. It follows that

\[
\dim_{mathbb F_2} C
=\dim_{mathbb F_2}M
=16(64+1)=1040.
\]

There are \(|A|2^{15}=2^{30}\) coordinates, so the block length is exactly
\(2^{30}\).

## Proof of minimum distance

For nonzero \(z\in F\), the word \(H(z)\) has weight at least \(2^{14}\).
Indeed, if some \(z_i\) with \(i\ge1\) is nonzero, then \(y\mapsto H(z)_y\)
is a nonconstant affine Boolean function and is balanced. If all those
coefficients vanish, then \(z=1\) and \(H(z)\) is the all-one word.

Let \(0\ne f\in M\). The polynomial \(f\) has at most \(64\) roots in \(A\),
so at least \(2^{15}-64=32704\) of its outer symbols are nonzero. Each such
symbol contributes at least \(2^{14}=16384\) ones after applying \(H\). Hence

\[
\begin{aligned}
\operatorname{wt}(\operatorname{Enc}(f))
&\ge (2^{15}-64)2^{14}\\
&=32704\cdot 16384\\
&=535{,}822{,}336.
\end{aligned}
\]

This applies to every nonzero message and proves the claimed minimum-distance
bound.

## Complete generator-matrix algorithm

Use the binary message basis

\[
\{\alpha^iX^j:0\le i\le15,\ 0\le j\le64\}.
\]

For row \((j,i)\) and column \((a,y)\), output

\[
G_{(j,i),(a,y)}=H(\alpha^i a^j)_y.
\]

Arithmetic in \(F\) is carryless binary polynomial arithmetic followed by
reduction modulo the displayed polynomial \(p\). Thus every entry is computed
by a bounded number of operations on 16-bit words. Enumerating all \(1040\cdot
2^{30}\) entries outputs the complete matrix in \(O(1040\cdot2^{30})=O(n)\)
fixed-word operations. The output itself contains \(1040n\) bits (130 GiB when
bit-packed), so the running time is polynomial in \(n\) and linear in the
output size up to a fixed constant.

## Parameter audit

\[
\begin{array}{c|c}
\text{quantity}&\text{value}\\ \hline
|F|&2^{16}=65{,}536\\
|A|&2^{15}=32{,}768\\
\text{outer dimension over }F&65\\
\text{outer distance}&\ge 2^{15}-64=32{,}704\\
\text{inner binary parameters}&[2^{15},16,2^{14}]_2\\
\text{binary length}&2^{15}\cdot2^{15}=2^{30}\\
\text{binary dimension}&65\cdot16=1040\\
\text{binary distance}&\ge32{,}704\cdot16{,}384=535{,}822{,}336\\
\text{rate}&1040/2^{30}=65/2^{26}
\end{array}
\]

## Verification

The independent review is recorded at
`research_state/campaign-epsilon-2-10-ultra/reviews/combinatorial-r002-07/verifier-codex-expert.json`.
The reviewer separately recomputed the field certificate, constituent
parameters, injectivity argument, distance product, rate, and full-matrix
runtime.

## Reference

Michael O. Rabin, “Probabilistic Algorithms in Finite Fields,” *SIAM Journal
on Computing* 9(2), 1980, 273–280, doi:10.1137/0209024. Only the deterministic
irreducibility criterion is used.
