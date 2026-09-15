# Independent verifier instructions

Audit one submission without relying on another verifier’s conclusion.

## Required checks

1. Confirm the final code is binary and linear.
2. Recompute the exact block length and require \(n=2^{30}\).
3. Recompute the certified dimension and rate.
4. Audit the proof that every nonzero codeword has weight at least \(535,822,336\).
5. Check the hypotheses and use of every imported theorem.
6. Check every constituent code and every transformation.
7. Confirm the construction is deterministic and symbolically reproducible.
8. Confirm the proof is understandable and complete at ordinary academic standards.
9. For an asymptotic claim, check the stated \(\Omega(\varepsilon^2)\) constant and uniform range.

Do not require proof-assistant-level formalization or reject for minor style. Do require repair when ambiguity conceals a real logical dependency.

## Verdict format

Return one of:

- `ACCEPT` — no unresolved mathematical obstruction; proof is sufficiently readable.
- `REPAIR REQUIRED` — potentially correct, but a specific gap or ambiguity must be fixed.
- `REJECT` — a fatal obstruction makes the claimed result false or inadmissible.

List the arithmetic you recomputed, the proof steps you audited, and all requested repairs. Label purely optional exposition suggestions as nonblocking polish.
