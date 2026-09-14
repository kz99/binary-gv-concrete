# Reed–Solomon plus RM(1,15)

## Theorem

There is an explicit binary linear code with parameters

\[
[2^{30},\,65,552,\,\ge469,762,048]_2.
\]

## Construction and proof

Over \(\mathbb F_{2^{16}}\), take a Reed–Solomon code with parameters

\[
[32,768,\,4,097,\,28,672]_{2^{16}}.
\]

Concatenate it with the binary first-order Reed–Muller code

\[
\operatorname{RM}(1,15)=[32,768,\,16,\,16,384]_2.
\]

Using an \(\mathbb F_2\)-linear identification \(\mathbb F_{2^{16}}\cong\mathbb F_2^{16}\), concatenation yields a binary linear code of length

\[
32,768^2=2^{30},
\]

dimension

\[
4,097\cdot16=65,552,
\]

and minimum distance at least

\[
28,672\cdot16,384=469,762,048.
\]

The claimed parameters follow. \(\square\)

## Verifier audit

- Reed–Solomon feasibility and distance: passed.
- Inner Reed–Muller parameters: passed.
- Concatenation identification: passed.
- Final parameter arithmetic: passed.
