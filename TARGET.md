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

The current verified baseline is \(\operatorname{RM}(1,30)\), with \(k=31\)
and \(d_{\min}=2^{29}\). A new concrete record therefore requires \(k\geq32\)
and a complete proof certificate.

The entropy-form Gilbert--Varshamov reference is

\[
R_{\mathrm{GV}}=1-h_2(511/1024)
=0.0000027517241633056023\ldots
\]

or \(k_{\mathrm{GV}}=2954.64132225\ldots\) at this blocklength. Thus
\(k\geq2955\) reaches the real-valued GV-rate reference.

The asymptotic aim is an explicit, symbolically specified family at relative
distance \(1/2-\varepsilon\) with rate \(\Omega(\varepsilon^2)\). Random
sampling is not an admissible construction method. Every claimed parameter
must follow from a human-readable mathematical proof.

The former \(7/16\) campaign is retained only as historical material under
`archive/target-7-16/`.
