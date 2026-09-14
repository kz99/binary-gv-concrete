# Contributor instructions: Binary GV Concrete

## 1. The research problem

Construct an explicit binary linear code

\[
C\subseteq\mathbb F_2^n
\]

at the single fixed block length

\[
n=2^{30}=1,073,741,824
\]

whose minimum distance satisfies

\[
d_{\min}(C)\ge \frac{7}{16}n=469,762,048.
\]

The score is the rigorously certified rate

\[
R=\frac{\dim C}{2^{30}}.
\]

Maximize this rate. Do not optimize a different block length, alphabet, distance, decoding radius, or asymptotic expression.

The current verified record is

\[
R\ge 0.0034351348876953125,
\qquad
\dim C\ge 3,688,448.
\]

Therefore a strict new record must certify

\[
\dim C\ge 3,688,449
\]

while preserving the exact length and required minimum distance.

For comparison, the binary Gilbert–Varshamov benchmark at relative distance \(7/16\) is

\[
R_{\mathrm{GV}}=1-h_2(7/16)=0.01130059171150255,
\]

or approximately \(12,133,918\) dimensions at this length. This is an existential reference, not an admissible submission.

In the usual high-distance notation

\[
\delta=\frac{1-\varepsilon}{2},
\]

our target is \(\varepsilon=1/8\).

## 2. What “explicit” means here

A submission must give a deterministic symbolic construction from first principles. A mathematical reader must be able to recover a generator or encoder from the stated data without sampling a random object or trusting an unproved search result.

State every choice that affects the code, including as applicable:

- the exact finite field and a deterministic representation of it;
- outer and inner codes and their exact parameters;
- function field, tower level, places, divisors, bases, and evaluation maps;
- graphs, rotation maps, walks, local codes, and ordering conventions;
- tensor, product, trace, subfield-subcode, concatenation, expander, or amplification operations;
- shortening, puncturing, expurgation, direct sums, repetitions, and zero padding; and
- the final deterministic map from messages to \(\mathbb F_2^{2^{30}}\).

It is not necessary to print an enormous generator matrix. A deterministic symbolic algorithm that produces it is enough.

The following do **not** qualify as a leaderboard construction:

- a random generator matrix or random inner code;
- “choose a good code” justified only by probability;
- Monte Carlo evidence;
- a numerical search with no structural proof of the winning object;
- an asymptotic family whose hidden constants are not instantiated at \(n=2^{30}\);
- a distance estimate based only on sampled codewords; or
- a construction at a nearby length without a proved exact-length transformation.

Computation may check arithmetic, factor polynomials, enumerate a genuinely small symbolic constituent, or help discover a proof. It may not replace the mathematical distance proof.

## 3. What must be proved

Every submission needs a proof certificate in `proofs/<submission-id>.md`. It must establish:

1. **Binary linearity.** The final object is a linear subspace of \(\mathbb F_2^{2^{30}}\).
2. **Exact length.** The final block length is exactly \(1,073,741,824\).
3. **Certified dimension.** The code has dimension at least the claimed integer \(k\).
4. **Minimum distance.** Every nonzero codeword has Hamming weight at least \(469,762,048\).
5. **Explicitness.** All construction choices are deterministic and reproducible.
6. **External inputs.** Every theorem imported from the literature is stated precisely and cited to a stable source.
7. **Parameter accounting.** All products, floors, ceilings, losses, and padding amounts are shown explicitly.

The proof should read like a concise academic mathematical note. It must be understandable and complete enough to audit, but it does not need proof-assistant-level formality. Minor style defects are not grounds for rejection.

Use [`proofs/SUBMISSION_TEMPLATE.md`](../proofs/SUBMISSION_TEMPLATE.md).

## 4. Promising ways to improve the record

These are suggestions, not restrictions.

### Improve the inner binary code

The current record concatenates an algebraic-geometry outer code over \(\mathbb F_{256}\) with

\[
\operatorname{RM}(1,7)=[128,8,64]_2.
\]

A structurally explicit inner code with a better rate–distance tradeoff, together with a compatible outer alphabet and exact proof, may improve the final score.

### Improve the outer code or its finite instantiation

Optimize the exact Garcia–Stichtenoth tower level, intermediate densification step, divisor, evaluation set, and padding loss. A different explicit AG tower or exact algebraic code is also admissible.

### Use algebraic alphabet reduction

Trace codes, subfield subcodes, concatenation variants, and multilevel concatenation may preserve more of a nonbinary AG code’s rate. All binary distance and dimension losses must be proved at the concrete target.

### Instantiate high-distance explicit-code constructions

Ta-Shma-style bias amplification, wide-replacement products, free expander walks, and related small-bias constructions are directly relevant because \(\delta=7/16=(1-1/8)/2\). The main challenge is to expose every constant and floor sufficiently sharply at \(n=2^{30}\).

### Combine methods

Possible hybrids include AG outer codes with structured inner-code families, expander distance amplification with algebraic base codes, or exact shortening/padding schemes. Every transformation must retain a human-readable distance proof.

## 5. Repository workflow

The source repository is <https://github.com/kz99/binary-gv-concrete>.

1. Fork the repository and create a branch named `submission/<short-id>`.
2. Copy `proofs/SUBMISSION_TEMPLATE.md` to `proofs/<short-id>.md` and write the proof certificate.
3. Add the candidate to `data/records.json` with status `under-review`. Do not rank it and do not mark it verified.
4. Add reusable lemma statements or research directions to the `research` section of `data/records.json` when useful.
5. Run the data validator and dashboard build.
6. Open a pull request titled `Submission: <construction name>`.
7. In the pull-request description, give the certified rate, dimension, distance, proof path, and a one-paragraph description of what is new.
8. Respond to mathematical questions from the verifier agents. Keep proof repairs in the same pull request.

Local checks from the repository root:

```bash
node scripts/validate-data.mjs
cd dashboard
pnpm install
pnpm build
```

## 6. Data entry for a new submission

Use a record of this form in `data/records.json`:

```json
{
  "rank": null,
  "id": "your-short-id",
  "name": "Descriptive construction name",
  "shortName": "Short name",
  "authors": "Contributor names",
  "date": "YYYY-MM-DD",
  "blockLength": 1073741824,
  "dimension": 3688449,
  "minimumDistance": 469762048,
  "rate": 0.003435135819017887,
  "rateType": "certified_lower_bound",
  "relativeDistance": 0.4375,
  "status": "under-review",
  "verification": {
    "arithmetic": "pending",
    "proof": "pending",
    "reviewers": 0,
    "agents": [],
    "writing": "pending",
    "summary": "Awaiting two independent reviews.",
    "reviews": []
  },
  "construction": "One-paragraph concrete description.",
  "proofPath": "proofs/your-short-id.md",
  "tags": ["symbolic"]
}
```

Compute `rate` as the claimed certified dimension divided by exactly `1073741824`. If only a lower bound on dimension is proved, use `certified_lower_bound`. Use `exact` only when exact dimension is proved.

## 7. Verification and publication

A submission does not appear on the main leaderboard merely because a pull request is open or merged.

Two distinct AI verifier agents independently read the proof. Neither verifier should rely on the other verifier’s conclusion. Each verifier checks:

- admissibility and deterministic explicitness;
- every concrete parameter and numerical identity;
- linearity, exact block length, dimension, and minimum distance;
- applicability of every cited theorem;
- effects of concatenation, shortening, puncturing, padding, or other transformations; and
- whether the proof is understandable at ordinary academic standards.

The verifiers should distinguish:

- **fatal obstruction:** the claimed result is false or the construction is inadmissible;
- **repair required:** a real but local gap, ambiguity, missing hypothesis, or arithmetic error;
- **nonblocking polish:** optional exposition or style improvements.

They should not hold correct work hostage to ceremonial detail or low-level formalization.

After two independent acceptances:

1. record both reviews in `verification.reviews`;
2. set arithmetic, proof, and writing fields to `passed`;
3. set `reviewers` to at least `2` and list the distinct agent identifiers;
4. set status to `verified`;
5. sort verified entries by certified rate and assign ranks; and
6. run the validator and publish the observatory.

Any unresolved mathematical obstruction keeps the candidate off the leaderboard. Rejected and in-progress work may remain in the Research Notebook so later contributors can learn from it.

## 8. Literature map

Start with the survey, then follow the branch closest to your construction.

### Orientation and the high-distance regime

- Dean Doron, **Binary Codes with Distance Close to Half** (ECCC TR24-159, 2024). A focused survey of explicit binary codes in the regime \(\delta=1/2-\Theta(\varepsilon)\). <https://eccc.weizmann.ac.il/report/2024/159/>
- Amnon Ta-Shma, **Explicit, Almost Optimal, Epsilon-Balanced Codes** (STOC 2017), DOI 10.1145/3055399.3055408. Gives explicit rate \(\Omega(\varepsilon^{2+o(1)})\) in the high-distance regime. <https://www.cs.tau.ac.il/~amnon/Papers/T.STOC17.pdf>
- Gil Cohen and Itay Cohen, **Wide Replacement Products Meet Gray Codes: Toward Optimal Small-Bias Sets** (ECCC TR25-179, 2025). Improves the register-maintenance component of the Ta-Shma framework. <https://eccc.weizmann.ac.il/report/2025/179/>
- Jun-Ting Hsieh, Sidhanth Mohanty, and Rachel Yun Zhang, **Explicit Almost-Optimal ε-Balanced Codes via Free Expander Walks** (2026). Gives a different near-optimal amplification framework. <https://arxiv.org/abs/2601.12606>

### Concatenation and alphabet reduction

- Dean Doron, Jonathan Mosheiff, and Mary Wootters, **When Do Low-Rate Concatenated Codes Approach the Gilbert–Varshamov Bound?** (2024). Isolates outer-code conditions under which concatenation with a random inner code approaches GV; useful as a derandomization target, although random inner codes are not admissible here. <https://arxiv.org/abs/2405.08584>
- Jørn Justesen, **A Class of Constructive Asymptotically Good Algebraic Codes** (IEEE Transactions on Information Theory, 1972), DOI 10.1109/TIT.1972.1054893. Classical explicit concatenated-code construction. <https://doi.org/10.1109/TIT.1972.1054893>

### Algebraic-geometry codes

- M. A. Tsfasman, S. G. Vlăduţ, and T. Zink, **Modular Curves, Shimura Curves, and Goppa Codes, Better than Varshamov–Gilbert Bound** (1982), DOI 10.1002/mana.19821090103. Establishes the AG-code advantage over GV for suitable nonbinary alphabets. <https://doi.org/10.1002/mana.19821090103>
- Arnaldo Garcia and Henning Stichtenoth, **A Tower of Artin–Schreier Extensions of Function Fields Attaining the Drinfeld–Vlăduţ Bound** (Inventiones Mathematicae 121, 1995), DOI 10.1007/BF01884295. The function-field tower underlying the current concrete record. <https://doi.org/10.1007/BF01884295>
- Stéphane Ballet, Julia Pieltant, Matthieu Rambaud, and Jeroen Sijsling, **On the Tensor Rank of Multiplication in Finite Extensions of Finite Fields and Related Issues in Algebraic Geometry**. Contains explicit densified Garcia–Stichtenoth tower bounds used in the current certificate. <https://perso.telecom-paristech.fr/rambaud/articles/BPRS.pdf>
- Gil Cohen, Dean Doron, Noam Goldgraber, and Tomer Manket, **Tracing AG Codes: Toward Meeting the Gilbert–Varshamov Bound** (2025). Studies field trace as an algebraic alternative to ordinary concatenation. <https://arxiv.org/abs/2511.08788>

## 9. Current verified certificates

- [`proofs/gs-rm-baseline.md`](../proofs/gs-rm-baseline.md): the current densified Garcia–Stichtenoth plus Reed–Muller record.
- [`proofs/rs-rm-baseline.md`](../proofs/rs-rm-baseline.md): an elementary Reed–Solomon plus Reed–Muller baseline.

Read these for repository conventions, but do not assume their claims without checking them when your construction depends on them.

## 10. Pull-request checklist

- [ ] Exact binary length \(2^{30}\).
- [ ] Certified minimum distance at least \(469,762,048\).
- [ ] Rate computed from the certified integer dimension.
- [ ] Deterministic symbolic construction; no random sampling.
- [ ] Complete proof certificate in `proofs/`.
- [ ] Every external theorem precisely cited.
- [ ] All finite parameter losses shown.
- [ ] New JSON record begins `under-review`.
- [ ] Validator and dashboard build pass.
- [ ] Pull request explains the new mathematical idea.

