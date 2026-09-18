# Exact dimension at the proposed binary Hermitian cutoff

**Status: independently reviewed mathematical result. This is not a new record.**

Put \(q=1024\), \(Q=q^2=2^{20}\), \(F=\mathbb F_Q\), and
\[
n=q^3=1073741824,\qquad
s=\frac{q^3}{2}+q^2=537919488.
\]
Let \(X/F\) be the smooth Hermitian curve
\[
y^q+y=x^{q+1},
\]
with unique point at infinity \(P_\infty\), and let \(D\) be the sum of its \(n\) rational affine points. Write
\[
B=C_L(D,sP_\infty)\cap\mathbb F_2^n.
\]

**Theorem.** The binary dimension of \(B\) is exactly \(81\). In fact, writing \(T=\operatorname{Tr}_{F/\mathbb F_2}\), its words are exactly the evaluations of
\[
\varepsilon+T(a x)+T(b y)+T(cxy)+T(d x^{513}),
\qquad \varepsilon\in\mathbb F_2,\quad a,b,c,d\in F.
\]
Here the displayed expressions describe evaluations; the last two traces have the reduced representatives specified below. Every word has distance certificate
\[
d_{\min}\ge n-s=535822336.
\]
Consequently this particular direct binary subfield-subcode route cannot improve the verified dimension \(1040\).

## Function-field facts and the derivative bound

Let \(K=F(X)\) and \(A=F[x,y]/(y^q+y-x^{q+1})\). The ring \(A\) consists of functions regular away from \(P_\infty\). Every element has a unique expression as a sum of \(x^iy^j\), with \(i\ge0\) and \(0\le j<q\). Their pole orders
\[
\rho(x^iy^j)=qi+(q+1)j
\]
are distinct. In particular, every nonconstant element of \(A\) has pole order at least \(q\).

Define
\[
V=x^Q+x.
\]
Its divisor is \((V)=D-nP_\infty\). Indeed every \(x\in F\) has exactly \(q\) corresponding \(F\)-values of \(y\), and these affine zeros are simple. Thus an element of \(A\) vanishing at all the evaluation points is divisible by \(V\) in \(A\).

Let \(\partial=d/dx\) on \(K\). The equation of the curve gives \(\partial y=x^q\), so \(\partial A\subseteq A\). Also
\[
(dx)=(q^2-q-2)P_\infty.
\]
For completeness, the affine map to the \(x\)-line is étale because the defining equation has derivative one with respect to \(y\); hence \(dx\) has no affine zero or pole. Its divisor has degree \(2g-2=q^2-q-2\), proving the formula. For \(u\in L(tP_\infty)\), local differentiation therefore gives
\[
\rho(\partial u)\le t+q^2-q-1
\tag{1}
\]
when \(\partial u\ne0\). The kernel of \(\partial\) is \(K^2\), since \(F\) is perfect and \(x\) is a separating variable. If \(u\in A\) is a square in \(K\), its square root is also in \(A\), with half its pole order.

These standard Hermitian facts and the evaluation-code notation are also recorded in [El Khalfaoui–Nagy, Sections 2–3](https://arxiv.org/pdf/1906.10444). Their Theorem 5.1 treats the smaller cutoff \(n/2\); the argument below treats \(n/2+q^2\).

## Square-root reduction

Because \(s<n\), evaluation on \(L(sP_\infty)\) is injective. Identify \(B\) with the \(\mathbb F_2\)-space of functions \(f\in L(sP_\infty)\) taking binary values on \(D\). Such an \(f\) satisfies
\[
f^2+f=Vh,\qquad h\in L(2q^2P_\infty).
\tag{2}
\]
The case \(h=0\) means \(f\in\mathbb F_2\). Assume otherwise as needed in the pole comparisons.

Differentiating (2) gives
\[
\partial f=h+V\partial h.
\]
If \(\partial h\ne0\), its pole order is nonnegative because it lies in \(A\). The term \(V\partial h\) consequently has pole order at least \(n\), whereas \(h\) has pole order at most \(2q^2\). This contradicts (1), since \(s+q^2-q-1<n\). Hence
\[
\partial h=0,\qquad \partial f=h.
\]
Define \(h_1=h^{1/2}\) and \(f_1=(f+xh)^{1/2}\). These are in \(A\), and squaring verifies
\[
f_1^2+f_1=xh+x^{Q/2}h_1.
\]

Inductively, for \(1\le j\le9\), we obtain
\[
h_j=h^{1/2^j},\qquad
f_j^2+f_j=xh+x^{Q/2^j}h_j,
\tag{3}
\]
with
\[
\rho(h_j)\le\frac{2q^2}{2^j},\qquad
\rho(f_j)\le\frac{s}{2^j}.
\tag{4}
\]
Here is the entire induction check. For \(j\le8\), differentiating (3) gives
\[
\partial f_j=h+x^{Q/2^j}\partial h_j.
\]
If \(\partial h_j\ne0\), its second term has pole order at least \(n/2^j\). This exceeds both \(2q^2\) and \(s/2^j+q^2-q-1\). The tightest comparison is at \(j=8\):
\[
4q^2>3q^2+3q-1.
\]
Thus \(\partial h_j=0\), \(\partial f_j=h\), and we may set
\[
h_{j+1}=h_j^{1/2},\qquad f_{j+1}=(f_j+xh)^{1/2}.
\]
Taking the square root of the resulting identity proves (3) at \(j+1\). The pole bound in (4) follows because, throughout these steps,
\[
\rho(xh)\le q+2q^2\le s/2^j\quad(j\le8).
\]

At \(j=9\), we have
\[
h_9\in L(4qP_\infty),\qquad
\rho(f_9)\le q^2+2q,
\]
and
\[
\partial f_9=h+x^{2q}\partial h_9.
\tag{5}
\]
If \(\partial h_9\) is nonconstant, its pole order is at least \(q\). The second term of (5) then has pole order at least \(2q^2+q\), cannot cancel with \(h\), and violates
\[
\rho(\partial f_9)\le2q^2+q-1.
\]
Therefore \(\partial h_9\in F\).

The monomial basis of \(L(4qP_\infty)\) is
\[
1,x,x^2,x^3,x^4,y,xy,x^2y,y^2,xy^2,y^3.
\]
The nonconstant derivatives of \(x^3,y,xy,x^2y,xy^2,y^3\) have respective pole orders
\[
2q,\ q^2,\ q^2+q,\ q^2+2q,\ 2q+2,\ q^2+2q+2.
\]
They are distinct, so cannot cancel. We conclude
\[
h_9\in\langle1,x,x^2,x^4,y^2\rangle_F.
\tag{6}
\]
The map \(\Phi:f\mapsto h_9\) is \(\mathbb F_2\)-linear with kernel exactly the binary constants. In particular, (6) already gives the structural upper bound \(\dim_{\mathbb F_2}B\le101\).

## Four trace families

All traces in this section have coefficients in \(F\), and all representatives belong to \(A\).

For \(a,b,c,d\in F\), define
\[
\begin{aligned}
F_a&=T(ax),\\
G_b&=T(by),\\
J_c&=T(cxy)+c^{Q/2}Vx^{q/2},\\
M_d&=\sum_{i=0}^{19}d^{2^i}x^{r_i},\qquad
r_i\equiv(\tfrac q2+1)2^i\pmod{Q-1},\quad1\le r_i\le Q-1.
\end{aligned}
\tag{7}
\]
They evaluate to the traces appearing in the theorem. Their pole orders are bounded, respectively, by
\[
\frac n2,\qquad
\frac n2+\frac{q^2}{2},\qquad
\frac n2+\frac{q^2}{2}+\frac q2,\qquad
\frac n2+q^2=s.
\tag{8}
\]
For \(J_c\), reduce the terms with \(i\ge10\) using
\[
y^{2^i}=x^{(q+1)2^{i-10}}+y^{2^{i-10}}.
\]
Only \(i=19\) produces an \(x\)-exponent at least \(Q\), namely \(Q+q/2\); the correction in (7) replaces that monomial by \(x^{1+q/2}\). The largest remaining pole is the third number in (8).

For \(M_d\), the exponents \(r_i\) rotate two one-bits, initially in positions 0 and 9, around 20 positions. The two configurations with a bit in position 19 have other bits in positions 10 and 8. Consequently \(\max r_i=2^{19}+2^{10}=Q/2+q\), proving its pole bound.

Direct calculation gives the respective quotients \((f^2+f)/V\):
\[
\begin{array}{c|c|c}
f & h=(f^2+f)/V & \Phi(f)=h^{1/512}\\ \hline
F_a & a & a^{2048}\\
G_b & b x^q & b^{2048}x^2\\
J_c & c y^q+c^{Q/2}x^{q/2} & c^{2048}y^2+c^q x\\
M_d & d^{2q}x^{2q}+d x^{q/2} & d^4x^4+d^{2048}x
\end{array}
\tag{9}
\]
For the third row, use \(y^Q+y=x^qV\) and expand the correction term's square. For the fourth, all cyclic terms cancel except the two exponent wraps described above. The two differences are \(Vx^{2q}\) and \(Vx^{q/2}\), with coefficients \(d^{2q}\) and \(d\).

The coefficients of \(1,x^2,y^2,x^4\) in the four images in (9) range independently over \(F\), since each indicated Frobenius map is bijective. Together with the constant function, these families therefore give an 81-dimensional binary space in \(B\).

## Excluding the remaining coefficient

For any \(f\in B\), subtract suitable functions from the four families so that (6) reduces to
\[
\Phi(f)=\beta x.
\]
Thus
\[
f^2+f=(x^Q+x)\beta^{512}x^{512}.
\tag{10}
\]
We show that \(\beta=0\).

The extension \(K/F(x)\) is Galois with group \(y\mapsto y+c\), \(c\in\mathbb F_q\). The right-hand side of (10) is fixed by this group. Therefore \(f(x,y+c)+f(x,y)\) is a root of \(z^2+z=0\), hence is in \(\mathbb F_2\). These differences define an additive character of \(\mathbb F_q\), necessarily
\[
c\longmapsto\operatorname{Tr}_{\mathbb F_q/\mathbb F_2}(uc)
\quad\text{for some }u\in\mathbb F_q.
\]
Set \(U_u(y)=\sum_{i=0}^{9}(uy)^{2^i}\). Subtracting this polynomial makes \(r=f+U_u(y)\) invariant under the group, so \(r\in F(x)\). It satisfies
\[
r^2+r=\beta^{512}x^{Q+512}+\beta^{512}x^{513}+u x^{q+1}.
\tag{11}
\]
Since the right side is polynomial, \(r\) cannot have a finite pole and is therefore polynomial.

Modulo polynomials of the form \(v^2+v\), one may replace a term \(\lambda x^{2e}\) by \(\lambda^{1/2}x^e\). Reducing the first term of (11) nine times gives the odd-degree part
\[
\beta x^{2049}+\beta^{512}x^{513}+u x^{1025}.
\]
If \(\beta\ne0\), its highest exponent is the odd integer \(2049\). Such a reduced polynomial cannot be of the form \(v^2+v\): eliminating the even leading terms of an Artin–Schreier polynomial leaves no positive odd-degree term. This contradicts (11). Thus \(\beta=0\), and the residual \(f\) is a binary constant. This proves both the asserted description and \(\dim B=81\). \(\square\)

The 81-row generator is explicit if desired: choose a deterministic basis of \(F/\mathbb F_2\), use it for each of the four parameters in the theorem, and evaluate at all affine rational points in a fixed order. Enumerating all pairs in \(F^2\) and retaining those on the curve takes \(Q^2=n^{4/3}\) field tests, while writing the matrix takes \(81n\) trace evaluations. All field arithmetic and deterministic field construction are polynomial in \(n\). The code meets the distance target but is far below the existing dimension record; the useful contribution is the exact-dimension obstruction for this proposed route.
