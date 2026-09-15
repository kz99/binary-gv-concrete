# Epsilon = 2^-10 campaign

This is the prepared mixed-reasoning campaign for the active target
\(d_{\min}\geq(1/2-2^{-10})2^{30}=535{,}822{,}336\). Its only operating
objective is the largest possible verified dimension \(k\) at that target. It
has not been launched. The snapshot is public so the observatory can render its
initial queue and later show proposed, verified, and rejected submissions.

The first research round has four teams of ten: algebraic, combinatorial,
combinatorial-expander, and composition. Each ten-seat team uses the staged
[team research graph](team-research-graph.md): three complementary foundation
researchers, three builders, an explicitness engineer, a cross-team liaison,
and a bottleneck breaker feeding one integrator who also authors submissions.
The combinatorial-expander team stays focused on
expander, Ta-Shma-style, and other explicit balanced-code routes.
For this campaign, "explicit" is strict: an admissible candidate supplies a
deterministic algorithm that outputs its entire generator matrix in
\(n^{O(1)}\) time, with a runtime proof. Canonical exhaustive searches and
superpolynomial conditional-expectation selectors are archived as
non-admissible evidence, never leaderboard entries.
Every ten-seat research team mixes three ultra, four max, and three xhigh
researchers. GENIUS remains ultra; verifiers and synthesis roles run at xhigh.
GENIUS is deferred by default and runs only as an explicit integration
checkpoint:

```bash
PYTHONPATH=src python3 -m binary_gv_research genius-checkpoint configs/campaign-epsilon-2-10-ultra.yaml
```

Every substantive output is committed to the shared repository; researchers
read it and the message board before their next attempt. The loop continues
with fresh rounds until a candidate with \(k>31\) receives its independent
verifier acceptance.

Launch only when explicitly requested:

```bash
PYTHONPATH=src python3 -m binary_gv_research launch configs/campaign-epsilon-2-10-ultra.yaml
```
