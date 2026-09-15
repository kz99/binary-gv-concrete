# Binary GV concrete target

Construct an explicit binary linear code

\[
C\subseteq\mathbb F_2^{\,2^{30}}
\]

with

\[
d_{\min}(C)\geq \left(\frac12-2^{-10}\right)2^{30}
=535{,}822{,}336,
\]

and maximize its dimension \(k=\dim C\).

The historical baseline is \(\operatorname{RM}(1,30)\), with \(k=31\) and
\(d_{\min}=2^{29}\). The current verified record is the explicit
Reed–Solomon–affine concatenated code with \(k=1040\) and certified distance
\(535{,}822{,}336\). A new concrete record therefore requires \(k\geq1041\)
and a complete proof certificate.

The entropy-form Gilbert--Varshamov reference is

\[
R_{\mathrm{GV}}=1-h_2(511/1024)
=0.0000027517241633056023\ldots
\]

or \(k_{\mathrm{GV}}=2954.64132225\ldots\) at this blocklength. Thus
\(k\geq2955\) reaches the real-valued GV-rate reference.

The operating aim is to approach this concrete GV reference by increasing the
verified dimension \(k\) at the fixed distance. General asymptotic insight is
useful only insofar as it produces a better concrete code or a necessary lemma.
Random sampling is not an admissible construction method. Explicitness is a
hard requirement: a deterministic algorithm must output the entire
\(k\times n\) generator matrix in \(n^{O(1)}\) time, and the certificate must
prove that runtime bound. A canonical exhaustive search or
conditional-expectation enumeration is not admissible, regardless of whether
it uniquely specifies a finite code. Every claimed parameter must follow from
a human-readable mathematical proof.

The former \(7/16\) campaign is retained only as historical material under
`archive/target-7-16/`.
