# Agent protocol

Work only on the canonical target

\[
n=2^{30},\qquad d_{\min}\geq\left(\frac12-2^{-10}\right)n=535{,}822{,}336.
\]

Maximize the rigorously proved dimension \(k\). The current verified baseline
is \(\operatorname{RM}(1,30)\) with \(k=31\); a concrete record needs
\(k\geq32\). The GV reference is \(k\approx2{,}955\), not a construction
claim.  Explicit means that the complete \(k\times n\) generator matrix can
be output by a deterministic algorithm in \(n^{O(1)}\) time.  The proof note
must state the algorithm and prove this bound.  A canonical exhaustive search,
conditional-expectation recursion, or finite lookup whose running time is
superpolynomial in \(n\) is not an explicit construction and is ineligible,
even when it defines a unique code.

The sole operating objective is to improve the verified leaderboard: produce
the largest possible \(k\) at this fixed length and required distance. General
or asymptotic ideas are in scope only when they improve, or directly support a
proof of, a stronger concrete leaderboard candidate. Do not use random sampling
as a construction method.

## Runtime and coordination

Researchers, literature analysts, verifiers, lemma editors, roadmap authors,
and the GENIUS synthesizer run at `model_reasoning_effort="ultra"`. Share
lemmas and proof tools across roadmaps, while giving each researcher modest
preference for its assigned roadmap.

## Submission standard

1. Specify the construction symbolically and deterministically, with an
   algorithm that outputs every entry of a full generator matrix in
   \(n^{O(1)}\) time.
2. Prove binary linearity, exact length, dimension, and distance in a concise
   academic note under `proofs/`.
3. State all finite choices, floors, padding, and inherited-code parameters.
4. Add reusable lemma statements to `data/records.json`; statements should be
   minimal, with explanations in proofs.
5. Leave results as draft or under review. One independent acceptance can mark
   a submission verified.

The verifier starts as soon as a complete candidate is written. They recompute
parameters, audit real mathematical gaps, and check that a reader can follow
the proof. They should not reject correct work for minor stylistic or
low-level-formalization issues. An unfixable obstruction rejects a candidate; a
local repair should be requested instead.

Run the data validator and dashboard build before publication.
