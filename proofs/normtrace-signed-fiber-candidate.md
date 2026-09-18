# A norm–trace candidate with 1056 message bits

**Status: incomplete research candidate. The target distance is not proved. This is not an eligible leaderboard submission.**

Let \(F=\mathbb F_{2^{16}}\), let \(E=\mathbb F_4\subset F\), and write
\[
T=\operatorname{Tr}_{F/\mathbb F_2},\quad
t=\operatorname{Tr}_{F/E},\quad
\nu(x)=N_{F/E}(x)=x^{21845},\quad
\psi(c)=(-1)^{\operatorname{Tr}_{E/\mathbb F_2}(c)}.
\]
Take the full affine norm–trace evaluation set
\[
\Omega=\{(x,y)\in F^2:t(y)=\nu(x)\}.
\]
For \(f\in F[X]_{\le65}\), define
\[
\operatorname{Enc}(f)=(T(yf(x)))_{(x,y)\in\Omega}.
\]
The use of a trace fiber is inspired by the splitting mechanism of Artin–Schreier towers. The norm–trace curve itself is standard; see Janwa–Piñero, *On Parameters of Subfield Subcodes of Extended Norm-Trace Codes*, Advances in Mathematics of Communications 11 (2017), 379–388, [arXiv:1604.05777](https://arxiv.org/abs/1604.05777). No distance claim below is inherited from that paper.

**Lemma 1.** The image of \(\operatorname{Enc}\) is a binary linear code of length \(2^{30}\) and dimension \(1056\).

*Proof.* The relative trace is a nonzero \(E\)-linear map from an eight-dimensional space to \(E\), so each fiber has \(4^7=16384\) points. Consequently
\[
|\Omega|=65536\cdot16384=1073741824.
\]
Linearity is immediate. Suppose \(\operatorname{Enc}(f)=0\). The annihilator of \(\ker t\) under the nondegenerate binary trace pairing is \(E\): inclusion follows from trace transitivity, and both spaces have binary dimension two. Differences of points within each fiber therefore imply \(f(x)\in E\) for every \(x\in F\). The polynomial \(f^4+f\), of degree at most 260, vanishes at all 65536 elements of \(F\), so is identically zero. Thus \(f\) is a constant \(c\in E\). Its encoding is \(\operatorname{Tr}_{E/\mathbb F_2}(c\nu(x))\). Since the norm is onto \(E\), this vanishes for every \(x\) only if \(c=0\). The encoding is injective, and its binary dimension is \(66\cdot16=1056\). ∎

Define
\[
S(f)=\sum_{\substack{x\in F\\ f(x)\in E}}\psi(f(x)\nu(x)).
\]

**Lemma 2.** For every \(f\in F[X]_{\le65}\),
\[
\operatorname{wt}(\operatorname{Enc}(f))=2^{29}-8192S(f).
\]

*Proof.* The character sum over the affine fiber \(t(y)=\nu(x)\) is zero unless \(f(x)\in E\). In the latter case, trace transitivity makes the character constant, with value \(\psi(f(x)\nu(x))\). Each fiber has 16384 points. The total binary character sum is therefore \(16384S(f)\); weight is half of length minus character sum. ∎

The exact remaining condition is
\[
\boxed{S(f)\le128\quad\text{for every nonzero }f\in F[X]_{\le65}.}
\tag{*}
\]
It would give
\[
2^{29}-8192\cdot128=535822336.
\]
At present, (*) is neither proved nor disproved. For nonconstant \(f\), the elementary root count gives only \(|S(f)|\le260\), hence
\[
d_{\min}\ge534740992,
\]
which falls short by 1081344. Nonzero constant polynomials outside \(E\) give \(S=0\). Nonzero constants in \(E\) give
\[
S=1-21845=-21844,
\]
so they are not the distance obstruction. This is a one-sided distance question; replacing (*) by an absolute-value bound would incorrectly exclude those constants.

## A structured test family

Let \(U\subset F\) be a three-dimensional \(E\)-subspace, let \(a\notin U\), and put
\[
L_U(X)=\prod_{u\in U}(X-u),\qquad f(X)=L_U(X)/L_U(a).
\]
The subspace polynomial is \(E\)-linearized and has degree 64. The contributing set is exactly \(U+Ea\): it contains 256 points, all roots of the degree-256 polynomial \(f^4+f\). For \(c\in E^\times\), the points in \(ca+U\) have \(f(x)=c\). Substituting \(x=c(a+u)\) gives
\[
c\nu(x)=c\,c^8\nu(a+u)=\nu(a+u).
\]
Thus, with \(H=\{z\in F^\times:\nu(z)=1\}\),
\[
S(f)=64+3\sum_{u\in U}\psi(\nu(a+u))
     =6\,|(a+U)\cap H|-128.
\]
The [affine linearized certificate](normtrace-affine-linearized-certificate.md) now proves that these intersections have size at most 40, by complete exact finite computation. Consequently \(S(f)\le112\) in this subfamily. The same certificate covers every affine \(E\)-linearized polynomial \(c+a_0X+a_1X^4+a_2X^{16}+a_3X^{64}\), with a sharp bound of 112. This does not establish (*) for arbitrary degree-65 polynomials.

## Deterministic full generator

Choose the lexicographically first monic irreducible degree-16 polynomial over \(\mathbb F_2\), testing the 65536 possibilities with the deterministic polynomial-gcd irreducibility criterion. This bounded field-representation calculation is polynomial in the output length and is not a search for a code. Use the resulting polynomial basis \(e_0,\ldots,e_{15}\) and polynomial-basis ordering on \(F\).

```text
Construct F and its ordered binary basis e_0,...,e_15.
Omega = empty list.
For each ordered pair (x,y) in F^2:
    If sum(y^(4^i), i=0,...,7) = x^21845:
        Append (x,y) to Omega.
For j = 0,...,65:
    For b = 0,...,15:
        For (x,y) in Omega:
            Output sum((e_b*y*x^j)^(2^i), i=0,...,15).
        End this row.
```

Each output is a binary field element. The algorithm writes exactly
\[
1056\cdot1073741824=1133871366144
\]
entries. The coordinate enumeration uses \(65536^2=4n\) pair tests. Polynomial-basis arithmetic, exponentiation, and traces take \(O((\log n)^3)\) bit operations per evaluation using schoolbook operations. The total is \(O((n+kn)(\log n)^3)\), bounded conservatively by \(O(n^4)\) in the parameterized algorithm. The dimension and generator are explicit independently of the unresolved distance condition.
