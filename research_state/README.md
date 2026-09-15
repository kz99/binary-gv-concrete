# Autonomous campaign state

Each campaign has a durable directory containing submissions, independent
reviews, lemma-book edits, proof roadmaps, a GENIUS synthesis, status, and a
machine-readable snapshot of promising and doubly verified candidates.

The standard pilot is launched with:

```bash
PYTHONPATH=src python3 -m binary_gv_research launch configs/campaign-10-ultra.yaml
```

All official jobs run with `model_reasoning_effort="ultra"`.  Agent prompts,
schemas, final JSON responses, stderr, and launch metadata are retained under
the campaign directory.  Large ephemeral traces are ignored by Git.
