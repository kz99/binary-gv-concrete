# Contributing to Binary GV Concrete

## 1. Exact problem

Give a deterministic, explicitly described binary linear code

\[
C\subseteq\mathbb F_2^{2^{30}}
\]

with

\[
n=2^{30}=1{,}073{,}741{,}824,\qquad
d_{\min}(C)\geq\left(\frac12-2^{-10}\right)n=535{,}822{,}336.
\]

The leaderboard score is its dimension \(k=\dim C\). A construction is
**explicit only if** a deterministic algorithm outputs the entire \(k\times n\)
generator matrix in \(n^{O(1)}\) time. The proof must state that algorithm and
prove its runtime bound. Random sampling, probabilistic existence alone,
numerical searches, canonical exhaustive searches, and
conditional-expectation recursions with superpolynomial runtime are not
submissions.

## 2. Benchmarks

The historical starting point is \(\operatorname{RM}(1,30)\): \(k=31\) and
\(d_{\min}=2^{29}\). The current verified record is the explicit
Reed–Solomon–affine concatenated code with \(k=1040\). A new record needs
\(k\geq1041\).

For orientation, the entropy-form binary GV value is

\[
R_{\mathrm{GV}}=1-h_2(511/1024)
=0.0000027517241633056023\ldots,
\]

which corresponds to \(k\approx2954.6413\), hence \(k\geq2955\), at the
fixed length. It is an existential reference line, not a verified construction.

The operating objective is to raise the verified concrete dimension \(k\) as
far as possible toward the GV reference. General or asymptotic work is useful
only when it yields a better concrete construction or a lemma needed to prove
one.

## 3. What a submission contains

Add both of the following:

1. A JSON record under `data/records.json`, initially with status `under-review`.
2. A proof note under `proofs/` establishing the claimed length, binary
   linearity, dimension, distance, and explicitness.

The proof should be a normal concise mathematical note. Name all constituent
codes, maps, fields, restrictions, shortenings, puncturings, and padding. Show
all finite arithmetic. Cite invoked theorems precisely enough that a reader can
locate them.

The explicitness section must include pseudocode (or an equally precise
algorithm), an output-size accounting for all \(kn\) entries, and a proof of a
runtime \(n^c\) for a fixed constant \(c\). A generator specified only by a
finite optimization, an average over completions, or an unbounded search is
ineligible.

Lemmas must have minimal statements and no explanatory prose. Put explanation
in their proofs. If clarity requires it, split a lemma into smaller lemmas.

## 4. Promising directions

- explicit small-bias and epsilon-balanced codes;
- expander- or walk-based bias amplification with exact finite accounting;
- algebraic trace and character-sum constructions;
- structured concatenation or multilevel methods that retain near-half distance.

The point is a genuine proof of a structured construction, not a fitted
parameter table.

## 5. Example record

```json
{
  "id": "your-code-id",
  "name": "Your construction",
  "blockLength": 1073741824,
  "dimension": 1041,
  "minimumDistance": 535822336,
  "rate": 9.695068001747131e-7,
  "status": "under-review",
  "generatorMatrix": {
    "outputsFullMatrixInPolynomialTime": true,
    "algorithm": "Describe the deterministic matrix-generation algorithm.",
    "runtimeBound": "O(n^c) for a fixed constant c.",
    "runtimeProof": "Account for every output entry and preprocessing step."
  },
  "proofPath": "proofs/your-code-id.md"
}
```

The complete field-level example is in `SUBMISSION_EXAMPLE.json`.

## 6. Verification and publication

Open a pull request. One independent verifier agent starts reviewing as soon as
the complete candidate is available, recomputes the parameters, audits the
polynomial-time generator algorithm, and reads the proof. They accept ordinary
mathematical exposition and do not require formal proof-assistant detail, but
must reject a superpolynomial or merely canonical generator, as well as any
claim with an unfixable mathematical obstruction. One acceptance may set the
record status to `verified` and place it on the main leaderboard.

Run `node scripts/validate-data.mjs` and `cd dashboard && pnpm build` before
submitting.

## 7. Literature map

- Amnon Ta-Shma, *Explicit, Almost Optimal, Epsilon-Balanced Codes* (STOC 2017).
- Dean Doron, *Binary Codes with Distance Close to Half* (2024 survey).
- Gil Cohen and Itay Cohen, *Wide Replacement Products Meet Gray Codes* (2025).
- Doron, Mosheiff, and Wootters, *When Do Low-Rate Concatenated Codes Approach GV?* (2024).
- Cohen, Doron, Goldgraber, and Manket, *Tracing AG Codes: Toward Meeting GV* (2025).

Historical \(7/16\) material is archived and is not the active target.
