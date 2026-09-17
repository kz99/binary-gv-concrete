# The next first-GS quadratic intermediate over F1024

Let \(q=32\), \(K=\mathbb F_{q^2}=\mathbb F_{1024}\), and define
\[
H: y^q+y=x^{q+1},\qquad
X: z^q+z=(y/x)^{q+1},\qquad
Y: w^2+w=(zx/y)^{q+1}.
\]
All curves mean their smooth projective models. This is the first
Garcia–Stichtenoth tower through level three, followed by a quadratic
intermediate of level four. The recursion and the existence of its
elementary abelian intermediate levels are in Ballet–Pieltant–Rambaud–Sijsling,
*On some bounds for symmetric tensor rank of multiplication in finite
fields*, §2.1.1, p. 6 of the
[author version](https://perso.telecom-paristech.fr/rambaud/articles/BPRS.pdf).
All numbers below follow directly from the equations.

## Finite parameters

Write \(u=y/x\) and \(v=z/u\). On \(H\), the function \(u\) has
\(q\) simple poles, namely infinity and the \(q-1\) affine points
\((0,\beta)\), \(\beta\in\mathbb F_q^\times\). It has a zero of
order \(q\) at the origin. The extension \(X/H\) has degree \(q\),
with total ramification at the \(q\) poles and different exponent
\((q-1)(q+2)\) at each. Therefore
\[
2g_X-2=q(q(q-1)-2)+q(q-1)(q+2)=65408,
\qquad g_X=32705.
\]
Each Hermitian point with \(x\ne0\) splits into \(q\) points on
\(X\). The origin splits into the \(q\) points \(z=\beta\),
\(\beta\in\mathbb F_q\). The \(q\) poles are rational and
totally ramified. Hence
\[
N_X=(q^2-1)q^2+2q=1047616.
\]

On \(X\), \(v\) has a simple pole at each of the \(q\) places
above the poles of \(u\). It also has a pole of order \(q\) at the
\(q-1\) places over the Hermitian origin with \(z=\beta\ne0\).
There are no other poles. At the latter places, use \(x\) as a local
parameter. The defining equations give
\[
u=x^q+x^{q^2+q-1}+\cdots,
\quad z=\beta+u^{q+1}+\cdots,
\quad v^{q+1}=\beta^2x^{-q(q+1)}+\beta^2x^{-(q+1)}+\beta+O(x).
\]
The two negative terms are an Artin–Schreier coboundary:
\[
\left(\sum_{i=0}^4(\beta^2x^{-33})^{2^i}\right)^2+
\sum_{i=0}^4(\beta^2x^{-33})^{2^i}
=\beta^2x^{-1056}+\beta^2x^{-33}.
\]
After this local change of the extension generator, the residue of the
right-hand side is \(\beta\in\mathbb F_{32}\). Its absolute trace
from \(\mathbb F_{1024}\) is zero, so all these places are unramified
and split in \(Y/X\). All other unramified rational places also split:
where \(v\) is finite, \(v^{q+1}\in\mathbb F_q\).

Exactly the \(q\) simple poles ramify in \(Y/X\), each with
different exponent \(q+2=34\). The odd pole order \(q+1=33\)
also proves that this is a genuine quadratic extension. Consequently
\[
\begin{aligned}
g_Y&=2g_X-1+q(q+2)/2=65409+544=65953,\\
N_Y&=2N_X-q=2095232-32=2095200.
\end{aligned}
\]

## An actual, weak binary code

The functions \(1,x,y\) on \(Y\) have poles only at infinity, of
orders \(0,2048,2112\). Evaluate them at all other \(2095199\)
rational points and concatenate with \(\operatorname{RM}(1,9)\), the
binary affine \([512,10,256]\) code. Append \(1953\) zero blocks of
length 512. The resulting code has
\[
n=(2095199+1953)512=2^{30},\qquad k=30,
\]
and
\[
d\ge(2095199-2112)256=535830272=535822336+7936.
\]
This construction is explicit: enumerate affine points of \(H\), repeat
each with \(x\ne0\) 64 times, repeat the origin 64 times, and use
each other point with \(x=0\) once. This is the evaluation multiset
seen by \(1,x,y\) from the indicated distinct points of \(Y\).
For each of the 30 field-basis multiples of \(1,x,y\), output its
affine inner evaluation blocks and the padding. Field construction,
the \(1024^2\) candidate point checks, and all \(30n\) entries take
polynomial time, by the same elementary algorithm as in the double-cover
draft. No new record is claimed.

## A ceiling for degree-certified functional codes on this curve

**Lemma.** If a smooth curve over \(\mathbb F_Q\) has \(N\) rational
points and a rational point, then every divisor \(G\) with at least two
sections satisfies
\[
h^0(G)\le\deg G-\left\lceil\frac N{Q+1}\right\rceil+2.
\]

*Proof.* Subtract \((h^0(G)-2)P\) for a rational point \(P\). The
remaining divisor still has at least two sections, whose ratio gives a
nonconstant map to \(\mathbb P^1\) of degree at most
\(\deg G-h^0(G)+2\). Any degree-\(a\) map defined over
\(\mathbb F_Q\) has at most \(a(Q+1)\) rational points on its
source. Rearranging proves the claim. ∎

Here \(\lceil2095200/1025\rceil=2045\), since
\(2044\cdot1025=2095100<2095200\).
The affine inner code requires outer distance
\(535822336/256=2093056\). A degree-certified functional code on
\(Y\), even evaluating all its rational points, thus requires
\[
\deg G\le2095200-2093056=2144.
\]
The lemma bounds its outer dimension by
\(2144-2045+2=101\), and its binary dimension by 1010. Reserving a
rational pole reduces the ceilings to 100 and 1000. This argument permits
arbitrary divisors and evaluation subsets. It is restricted to the usual
degree distance certificate, distinct rational evaluation points, the
stated affine inner code, and zero padding; it does not exclude a stronger
distance theorem or a different architecture.
