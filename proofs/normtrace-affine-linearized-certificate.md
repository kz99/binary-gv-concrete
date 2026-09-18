# A finite certificate for the affine linearized norm–trace subcode

**Scope.** This note certifies one subcode of the incomplete dimension-1056 construction in [the candidate note](normtrace-signed-fiber-candidate.md). It does not prove the distance of that entire construction and is not a new leaderboard record. The geometric bound below is proved by complete exact finite computation, with an independently recomputed certificate.

Put
\[
F=\mathbb F_{2^{16}},\quad E=\mathbb F_4,\quad
t=\operatorname{Tr}_{F/E},\quad T=\operatorname{Tr}_{F/\mathbb F_2},\quad
\nu(x)=x^{21845},\quad \psi(c)=(-1)^{\operatorname{Tr}_{E/\mathbb F_2}(c)}.
\]
The coordinates and encoding are
\[
\Omega=\{(x,y)\in F^2:t(y)=\nu(x)\},\qquad
c_f=(T(yf(x)))_{(x,y)\in\Omega}.
\]
Each trace fiber has \(4^7=16384\) points, so \(|\Omega|=65536\cdot16384=2^{30}\). Fiber orthogonality gives
\[
\operatorname{wt}(c_f)=2^{29}-8192S(f),\qquad
S(f)=\sum_{x:f(x)\in E}\psi(f(x)\nu(x)).                 \tag{1}
\]
This is the signed-fiber mechanism of Proposition 5.1 in the user-supplied *Square-Root Character Sums on a Fixed Function-Field Tower*. Its distinction between a signed sum and the size of the exceptional set motivates this calculation.

## The finite geometric certificate

**Lemma 1.** If \(\dim_E U=3\), \(a\in F\), and \(r\in E^\times\), then
\[
|(a+U)\cap\nu^{-1}(r)|\le40.
\]

*Proof by complete finite computation.* We specify both the coverage argument and the exact computation. The implementation is [verify-normtrace-flats.cpp](../scripts/verify-normtrace-flats.cpp); the separate [witness checker](../scripts/verify-normtrace-flat-witness.py) uses direct polynomial arithmetic.

Represent field elements by their 16 binary coefficients modulo
\[
p(Z)=Z^{16}+Z^5+Z^3+Z^2+1\quad\text{(hexadecimal \(0x1002d\))}.
\]
The witness checker verifies \(Z^{2^{16}}=Z\pmod p\) and \(\gcd(p,Z^{2^8}-Z)=1\), the degree-16 irreducibility criterion. It also verifies that \(\alpha=Z\bmod p\) is primitive by testing the four prime divisors \(3,5,17,257\) of 65535. The exhaustive verifier generates all 65535 nonzero powers without premature repetition. Thus
\[
E=\{0,1,44234,44235\},\qquad \alpha^{21845}=44234.
\]
For \(x=\alpha^j\ne0\), its norm class is \(j\bmod3\). The program checks that \(1,\alpha,\ldots,\alpha^7\) form an \(E\)-basis by enumerating its 65536 distinct linear combinations.

Every three-space scales to contain 1. Such spaces correspond to two-spaces of \(F/E\), and their exact number is
\[
{7\brack2}_4=\frac{(4^7-1)(4^6-1)}{(4^2-1)(4-1)}=1490853.       \tag{2}
\]
Enumerate their unique two-row reduced row echelon matrices in the quotient basis \(\alpha,\ldots,\alpha^7\). For pivots \(i<j\), the pivot entries are 1, all earlier entries and the other pivot entry are zero, and each remaining entry runs through \(E\). The lifted rows \(a,b\) specify \(U=\operatorname{span}_E(1,a,b)\).

Its monic subspace polynomial is
\[
Q_U(X)=X^{64}+AX^{16}+BX^4+CX,\qquad C=1+A+B.
\]
The pair \((A,B)\) uniquely identifies \(U\). With
\[
D=(a^4+a)^3,\quad H=1+D,\quad s=b^{16}+Hb^4+Db,
\]
the recurrence \(Q_{W+Ev}=Q_W^4+Q_W(v)^3Q_W\) gives
\[
A=H^4+s^3,\qquad B=D^4+s^3H,\qquad C=s^3D.
\]
The implementation checks the polynomial on all 64 elements of each retained space and checks \(C=1+A+B\ne0\).

The desired maximum is invariant under \(U\mapsto dU^{2^h}\), for \(d\ne0\) and \(0\le h<16\): this map bijects affine cosets and permutes norm classes. The normalized spaces in the orbit of a space containing 1 are exactly
\[
(u^{-1}U)^{2^h},\qquad u\in U\setminus\{0\},\quad0\le h<16.
\]
Indeed, \(1\in dU^{2^h}\) forces \(d=u^{-2^h}\). Only one representative of each of the 21 \(E^\times\)-orbits of \(u\) is needed. The corresponding key is
\[
\bigl((Au^{-48})^{2^h},(Bu^{-60})^{2^h}\bigr).
\]
The program retains the first uncovered RREF space and marks this entire orbit. It asserts that distinct retained orbits are disjoint. Their sizes are

| Orbit size | Number |
|---:|---:|
| 21 | 1 |
| 84 | 4 |
| 168 | 40 |
| 336 | 4416 |

The weighted sum is 1490853, equal to (2). For each of the 4461 representatives, the program scans all 1024 cosets by retaining the smallest not-yet-visited field element and enumerating its 64 translates. All three nonzero norm counts are computed exactly. A linear three-space has 21 elements of each norm class: each of its 21 scalar orbits contains one of each. For nonzero cosets the computed maxima are

| Maximum | Number of representatives |
|---:|---:|
| 30 | 12 |
| 32 | 1603 |
| 34 | 2289 |
| 36 | 503 |
| 38 | 51 |
| 40 | 3 |

This exhausts every space, coset, and nonzero norm class. The exact point-count loop makes \(4461\cdot65536=292356096\) visits. More generally, for fixed subspace dimension three over \(E=\mathbb F_4\), direct normalized-space enumeration and coset counting use \(O(Q^3\operatorname{polylog}Q)\) bit operations for \(Q=|F|\). No search selects any code or generator.

An independent implementation, using canonical row-space keys rather than subspace-polynomial keys and binary quotient syndromes rather than coset traversal, reproduced the entire coverage and both tables. The bound is sharp: \(U=\operatorname{span}_E(1,10,15508)\), \(a=306\), \(r=44234\) gives 40 points. ∎

## The resulting subcode

**Lemma 2.** For every nonzero
\[
f(X)=c+a_0X+a_1X^4+a_2X^{16}+a_3X^{64},\qquad c,a_i\in F,
\]
one has \(S(f)\le112\).

*Proof.* If the linearized part \(L\) is nonzero, its kernel is an \(E\)-space of dimension \(r\le3\). The affine space \(c+\operatorname{im}L\) meets \(E\) in zero, one, or four elements. Thus at most 64 inputs contribute unless \(r=3\) and all four values occur.

In that case each fiber has 64 points. The zero-valued fiber contributes 64. A fiber with value \(\lambda\in E^\times\) avoiding zero contributes
\[
2|f^{-1}(\lambda)\cap\nu^{-1}(\lambda^{-1})|-64\le16
\]
by Lemma 1. If it contains zero, it is the linear kernel, so its contribution is \(2(1+21)-64=-20\). Hence \(S(f)\le64+3\cdot16=112\). Nonzero constants outside \(E\) have \(S=0\), while nonzero constants in \(E\) have \(S=1-21845=-21844\). ∎

**Theorem.** The displayed affine linearized family gives a binary linear code with parameters
\[
[1073741824,80,535953408]_2.
\]

*Proof.* Binary linearity follows from the trace. If \(c_f=0\), differences inside every trace fiber force \(f(x)\in E\) for every \(x\in F\). Thus \(f^4+f\), of degree at most 256, vanishes identically. It follows that \(f\) is a constant in \(E\), and norm surjectivity and trace nondegeneracy force this constant to be zero. Therefore the encoding is injective, of dimension \(5\cdot16=80\).

Equation (1) and Lemma 2 give distance at least
\[
536870912-8192\cdot112=535953408=535822336+131072.
\]
The bound is attained. In the field representation above, the witness checker verifies
\[
f(X)=20305X^{64}+48468X^{16}+44617X^4+30407X
\]
has \(S(f)=112\). It enumerates 256 distinct roots of \(f^4+f\), its full root set by the degree bound, and evaluates every sign using direct polynomial arithmetic. ∎

This theorem covers \(2^{80}-1\) nonzero messages. It excludes neither arbitrary binary-linearized polynomials with exponents \(2,8,32\) nor general polynomials of degree at most 65.

## Full generator and reproduction

The generator uses the fixed field above and basis \(1,\alpha,\ldots,\alpha^{15}\). Order field elements by their binary coefficients and use lexicographic coordinate order.

```text
Construct the field F modulo p and its binary basis.
Enumerate all (x,y) in F^2 with t(y)=x^21845, in order.
For j in (0,1,4,16,64):
    For b in (0,...,15):
        Output the row T(alpha^b * y * x^j) at every coordinate.
```

At \(j=0\), use \(x^0=1\), including \(x=0\). The algorithm writes exactly \(80\cdot2^{30}=85899345920\) binary entries. Coordinate enumeration uses \(65536^2=4n\) pair tests. Schoolbook field arithmetic, exponentiation, and traces give \(O((n+80n)(\log n)^3)\) bit operations, in particular \(O(n^4)\). The finite geometric certificate is not needed to select the generator. Changing to the field model in the dimension-1056 candidate gives an isomorphic code by a coefficient isomorphism and coordinate permutation.

From the repository root, reproduce the finite certificate without storing a generator matrix:

```sh
clang++ -std=c++17 -O3 scripts/verify-normtrace-flats.cpp -o /tmp/verify-normtrace-flats
/tmp/verify-normtrace-flats /tmp/normtrace-flat-representatives.csv
python3 scripts/verify-normtrace-flat-witness.py
```

Assertions must remain enabled. The representative CSV has 4461 data rows and SHA-256 `f711890325783b475353a1e935afe2482bc60e2f73ab5fc89957863f6543485f`.
