# Autonomous campaign state

Each campaign has a durable directory containing submissions, independent
reviews, lemma-book edits, proof roadmaps, a GENIUS synthesis, status, and a
machine-readable snapshot of promising and doubly verified candidates.

The current campaign is prepared, but is not launched, with:

```bash
PYTHONPATH=src python3 -m binary_gv_research launch configs/campaign-epsilon-2-10-ultra.yaml
```

All official jobs run with `model_reasoning_effort="ultra"`.  Agent prompts,
schemas, final JSON responses, stderr, and launch metadata are retained under
the campaign directory.  Large ephemeral traces are ignored by Git.

The former \(7/16\) campaign is preserved under `research_state/archive/target-7-16/`.
