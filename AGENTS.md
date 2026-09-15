# Agent protocol

This repository studies explicit binary linear codes at the single fixed target

\[
n=2^{30},\qquad d_{\min}\ge 469,762,048=\frac{7}{16}n.
\]

The score is the rigorously proved rate \(R=k/n\). Do not optimize or rank by a different quantity.

Read `how_to_contribute/CONTRIBUTOR_INSTRUCTIONS.md` before proposing or reviewing a submission. It is the canonical public specification for this project.

## Campaign runtime

Every autonomous role in the official campaign---researcher, literature analyst,
verifier, lemma editor, roadmap author, and GENIUS synthesizer---must run with
`model_reasoning_effort="ultra"`.  The campaign launcher rejects any other
reasoning setting.

The standard Garcia--Stichtenoth plus binary Hadamard/RM(1,7) template has a
known rate envelope at relative distance \(7/16\).  With an outer alphabet
\(\mathbb F_{2^m}\), even \(m\), the usual optimal-tower/Riemann--Roch
accounting and the inner code
\(\operatorname{RM}(1,m-1)=[2^{m-1},m,2^{m-2}]_2\) give

\[
R_{\mathrm{template}}(m)
=\frac{m}{2^{m-1}}
\left(\frac18-\frac{1}{2^{m/2}-1}\right)_+.
\]

This expression is maximized at \(m=8\), where it equals
\(7/1920\approx0.0036458333333\).  This is a ceiling for the standard
certified template and its parameter-optimization argument, not a universal
impossibility theorem for every code extracted from a GS tower.  Agents may
close the finite-size gap up to this value, but the primary objective is to
cross \(7/1920\) using a genuinely stronger inner code, alphabet-reduction
method, multilevel construction, expander amplification, trace/subfield
argument, or another rigorously explicit mechanism.

## Research agents

1. Work with deterministic, symbolically specified constructions. Do not use random sampling as a construction method.
2. State every concrete parameter choice: fields, constituent codes, tower levels, divisor degrees, shortening, puncturing, padding, and identifications.
3. Write an academic-style proof note in `proofs/` establishing exact block length and dimension and the claimed minimum-distance lower bound.
4. Put reusable lemma statements and exploratory directions in the `research` section of `data/records.json`. This material appears only in the Research Notebook.
5. New entries begin as `draft` or `under-review`. Never mark your own construction `verified`.

## Proof-writing standard

The proof must be clear and complete enough that a mathematical reader can reconstruct the argument, check the parameter arithmetic, and locate every invoked theorem. Prefer concise theorem statements and put explanation in the proof.

Do not add ceremonial detail or line-by-line formalization. Minor stylistic imperfections are not a reason to reject an otherwise correct and understandable proof.

## Verification gate

A record may be marked `verified` only when two separate AI verifier agents independently:

- recompute the concrete parameters;
- check the mathematical proof for genuine gaps;
- confirm the construction is admissible and deterministic;
- confirm the proof meets the pragmatic writing standard; and
- record an acceptance in the review history.

Any unresolved mathematical obstruction blocks publication. A verifier should suggest a repair when the problem is local and fixable. The main leaderboard automatically filters out every non-verified entry.

## Publication invariant

Run `node scripts/validate-data.mjs` and build the dashboard before publishing. The validator enforces exact length, minimum distance, rate arithmetic, proof presence, two distinct verifier identities, and the writing pass.
