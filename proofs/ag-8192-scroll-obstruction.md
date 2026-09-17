# The degree-512 AG route over \(\mathbb F_{8192}\)

**Status: independently accepted proof tool. This is an obstruction, not a new code.**

The proposed outer parameters \([262144,81,261632]_{8192}\), concatenated with \(\operatorname{RM}(1,12)=[4096,13,2048]_2\), would give
\[
n=262144\cdot4096=1073741824,\qquad k=81\cdot13=1053,
\qquad d\ge261632\cdot2048=535822336.
\]
The theorem below excludes obtaining these parameters from the ordinary divisor-degree distance bound for a rational-point AG evaluation code. It does not exclude arbitrary outer codes or stronger distance certificates for divisors of larger degree.

**Theorem.** Let \(X/\mathbb F_{8192}\) be a smooth projective geometrically integral curve with \(\#X(\mathbb F_{8192})\ge262144\). If \(G\) is a rational divisor with \(\deg G\le512\), then \(\ell(G)\le80\).

**Lemma 1.** A complete base-point-free birational linear series of projective dimension \(r\ge3\) in characteristic two has non-strange image.

*Proof.* Extend constants to an algebraic closure. If the image is strange, choose projective coordinates with nucleus \((0:1:0:\cdots:0)\). Dividing the sections by the first section gives a basis \(1,x,y_2,\ldots,y_r\) of \(L(E)\) for an effective divisor \(E\), with \(dx\ne0\) and \(dy_i=0\). These derivative assertions follow directly from the tangent lines passing through the nucleus; birationality ensures that not all coordinate differentials vanish. The kernel of the differential in a one-variable function field over a perfect field of characteristic two is its square subfield. Write \(y_i=z_i^2\).

The space \(A=\langle1,z_2,\ldots,z_r\rangle\) has dimension \(r\) and lies in \(L(\lfloor E/2\rfloor)\). Thus the span of its pairwise products lies in \(L(E)\). At a smooth point, a valuation-adapted basis of \(A\) has \(r\) distinct integer valuations. Their sumset has at least \(2r-1\) elements, giving at least \(2r-1\) independent products. Consequently \(r+1=\ell(E)\ge2r-1\), a contradiction. \(\square\)

**Lemma 2.** If \(\Gamma\subset\mathbb P^{r-1}\) consists of \(d\) spanning points in uniform position, its Hilbert function satisfies
\[
h_\Gamma(j+1)\ge\min\{d,h_\Gamma(j)+r-1\}.
\]

*Proof.* Put \(t=\min\{d,h_\Gamma(j)+r-1\}\), and select \(t\) points. For each selected point \(P\), partition the other \(t-1\) points into sets of sizes at most \(h_\Gamma(j)-1\) and \(r-1\). Uniform position supplies a degree-\(j\) form vanishing on the first set and not at \(P\), and a linear form with the corresponding property for the second set. Their product separates \(P\) from the other selected points. The resulting \(t\) evaluations are independent. \(\square\)

*Proof of the theorem.* Suppose \(\ell(G)=r+1\ge81\). Replace \(G\) by a linearly equivalent effective divisor and remove its fixed divisor, obtaining a base-point-free divisor \(E\) of degree \(a\le512\). Let \(f:X\to Y\) be the map to the normalization of its projective image, let \(\delta=\deg f\), and let \(e\) be the degree of that image. Then \(a=\delta e\), \(e\ge r\ge80\), and \(1\le\delta\le6\). The hyperplane divisor \(H\) on \(Y\) satisfies \(E=f^*H\). Its series is complete: pullback injects \(L(H)\) into \(L(E)\), and the \(r+1\) coordinate sections already attain the latter dimension. Lemma 1 therefore applies to the image of \(Y\).

Kadets, Theorem 1.4 [1], gives sectional monodromy containing \(A_e\) for this non-strange curve in projective dimension at least four. Consequently a general hyperplane section is in uniform position. Lemma 2 and the usual Hilbert-function genus calculation give
\[
g(Y)\le\pi(e,r),\qquad
\pi(e,r)=\binom{s}{2}(r-1)+s\epsilon,
\quad e-1=s(r-1)+\epsilon,\quad0\le\epsilon<r-1.
\]
Indeed \(h_\Gamma(j)\ge\min\{e,j(r-1)+1\}\), and the arithmetic genus of the projective image is at most \(\sum_{j\ge1}(e-h_\Gamma(j))\); its geometric genus is no larger. This proves the displayed formula without assuming that the image is smooth.

Serre's bound [2] is \(\#Y(\mathbb F_{8192})\le8193+181g(Y)\), since \(\lfloor2\sqrt{8192}\rfloor=181\). Every rational point of \(X\) maps to a rational point of \(Y\), with at most \(\delta\) points in a fiber. The cases \(\delta\ge2\) therefore give:

| \(\delta\) | \(\lfloor512/\delta\rfloor\) | \(\pi(\lfloor512/\delta\rfloor,80)\) | Upper bound on \(\#X(\mathbb F_{8192})\) |
|---:|---:|---:|---:|
| 2 | 256 | 291 | 121728 |
| 3 | 170 | 101 | 79422 |
| 4 | 128 | 48 | 67524 |
| 5 | 102 | 22 | 60875 |
| 6 | 85 | 5 | 54588 |

All contradict the hypothesis, so \(\delta=1\). Serre's bound now gives
\[
g(X)\ge\left\lceil\frac{262144-8193}{181}\right\rceil=1404.
\]
The equalities
\[
\pi(512,80)=1407,\quad\pi(511,80)=1401,
\quad\pi(512,81)=1386
\]
force \(a=512\), \(r=80\), and \(1404\le g(X)\le1407\).

Write \(C\subset\mathbb P^{80}\) for the projective image and \(\Gamma\) for a general hyperplane section. If \(h_\Gamma(2)\ge160\), Lemma 2 gives
\[
(h_\Gamma(1),\ldots,h_\Gamma(7))\ge
(80,160,239,318,397,476,512).
\]
The genus calculation would then give
\[
g(X)\le432+352+273+194+115+36=1402,
\]
a contradiction. Hence \(h_\Gamma(2)=159=2\cdot79+1\). Choose 161 points \(\Gamma_0\subset\Gamma\). Uniform position gives \(h_{\Gamma_0}(2)=159\), and the arbitrary-field Castelnuovo lemma [3, Theorem 6, with \(k=80\)] puts \(\Gamma_0\) on a rational normal curve \(R\) of degree 79. The spaces of quadrics through \(\Gamma\), through \(\Gamma_0\), and through \(R\) all have equal dimension; the first and third lie in the second, so they coincide. The quadrics through a rational normal curve generate its homogeneous ideal, so their common zero scheme is exactly \(R\).

The curve \(C\) is linearly normal, since its hyperplane sections pull back to the complete 81-dimensional space on \(X\). Therefore \(H^1(\mathcal I_C(1))=0\), and all quadrics through \(\Gamma\) lift to quadrics through \(C\). Let \(Z\) be the common zero scheme of the latter quadrics. Scheme-theoretically \(Z\cap H=R\) for a general hyperplane \(H\). Thus \(Z\) has a unique reduced surface component \(S\), geometrically integral of degree 79. Moreover \(C\subset S\): otherwise a general hyperplane would meet \(C\) outside \(S\), contrary to \(Z\cap H=R\). Since \(C\) is nondegenerate, so is \(S\). This also proves that \(S\) is defined over \(\mathbb F_{8192}\): it is the unique geometric surface component of a scheme defined by rational quadrics.

The classification of surfaces of minimal degree [4] makes \(S\) a rational normal scroll, possibly a cone; the Veronese exception has degree four. On the scroll, or on its minimal resolution in the cone case, write the strict transform of \(C\) as \(tH+bF\), where \(H^2=79\), \(H\cdot F=1\), and \(F^2=0\). Here \(t\ge1\) is the degree of the ruling restricted to the normalization \(X\), and
\[
79t+b=512,\qquad K_S=-2H+77F.
\]
Adjunction bounds the geometric genus by
\[
g(X)\le p_a(\widetilde C)
 = (t-1)\left(511-\frac{79t}{2}\right).
\]
The right side is a concave quadratic in \(t\), with maximum between 6 and 7. Its values at 6, 7, and 8 are 1370, 1407, and 1365. Thus \(g(X)\ge1404\) forces \(t=7\).

The cone case is impossible: on its resolution \(\mathbb F_{79}\), with negative section \(C_0\), the strict transform has class \(tC_0+512F\). It is distinct from \(C_0\), so its intersection \(512-79t\) with \(C_0\) is nonnegative, forcing \(t\le6\).

The smooth scroll of degree 79 has a unique positive-dimensional family of ruling lines. Its component in the Fano scheme descends to \(\mathbb F_{8192}\); normalize it to obtain a smooth genus-zero curve \(B\). The incidence correspondence gives the ruling over that field, and its restriction extends to a degree-seven morphism from the smooth projective curve \(X\) to \(B\). A rational point of \(X\) gives one on \(B\), so \(B\simeq\mathbb P^1\). Consequently
\[
\#X(\mathbb F_{8192})\le7(8192+1)=57351<262144,
\]
the final contradiction. \(\square\)

For concatenation with \(\operatorname{RM}(1,12)\), exact length fixes the number of outer rational evaluation points at 262144. The standard product distance certificate requires \(\deg G\le512\). Evaluation is injective in that range, so the theorem bounds the binary dimension by \(13\cdot80=1040\). No matrix-generation claim is made: no new code is constructed here.

## References

1. B. Kadets, *Sectional monodromy groups of projective curves*, Theorem 1.4; [author's preprint, arXiv:1809.07293](https://arxiv.org/abs/1809.07293). Only the theorem for non-strange curves in projective dimension at least four is used.
2. J.-P. Serre, *Sur le nombre des points rationnels d'une courbe algébrique sur un corps fini*, C. R. Acad. Sci. Paris Sér. I Math. **296** (1983), 397–402; [1983–84 course summary](https://www.college-de-france.fr/sites/default/files/media/document/2023-03/1983-1984_serre.pdf).
3. S. Ball and V. Pepe, *On varieties defined by large sets of quadrics and their application to error-correcting codes*, Section 4, Theorem 6, p. 14 of [arXiv:1904.12797v2](https://arxiv.org/abs/1904.12797). The proof is over an arbitrary field.
4. D. Eisenbud, M. Green, K. Hulek, and S. Popescu, *Small schemes and varieties of minimal degree*, Theorem 0.1, p. 2 of [arXiv:math/0404517v5](https://arxiv.org/abs/math/0404517). The base field is algebraically closed with unrestricted characteristic.

The square-root argument in Lemma 1 is motivated by the coordinate argument in J. F. Voloch, *Special divisors of large dimension on curves with many points over finite fields*, Portugaliae Mathematica **68** (2011), 103–107, Lemma 2.1 ([paper](https://ems.press/content/serial-article-files/44668)). Completeness supplies the stronger conclusion used here.
