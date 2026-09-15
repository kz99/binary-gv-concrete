# Epsilon = 2^-10 campaign

This is the prepared ultra-reasoning campaign for the active target
\(d_{\min}\geq(1/2-2^{-10})2^{30}=535{,}822{,}336\). Its only operating
objective is the largest possible verified dimension \(k\) at that target. It
has not been launched. The snapshot is public so the observatory can render its
initial queue and later show proposed, verified, and rejected submissions.

The first research round has three teams of ten: algebraic, combinatorial, and
composition. Every substantive output is committed to the shared repository;
researchers read it and the message board before their next attempt. The loop
continues with fresh rounds until a candidate with \(k>31\) receives both
independent verifier acceptances.

Launch only when explicitly requested:

```bash
PYTHONPATH=src python3 -m binary_gv_research launch configs/campaign-epsilon-2-10-ultra.yaml
```
