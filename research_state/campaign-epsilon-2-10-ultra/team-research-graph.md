# Ten-seat team research graph

Each named team follows this directed acyclic graph.  The four teams use
different construction families, but all durable outputs, lemma-book entries,
and message-board posts are shared across the campaign.

```mermaid
flowchart TD
  S1[1. Landscape scout] --> A[4. Construction architect]
  S2[2. Construction-component investigator] --> A
  S3[3. Obstruction and parameter auditor] --> A
  S1 --> O[5. Finite-parameter optimizer]
  S2 --> O
  S3 --> O
  S1 --> P[6. Proof-lemma builder]
  S2 --> P
  S3 --> P
  A --> E[7. Explicitness engineer]
  O --> E
  A --> C[8. Cross-team lemma and component liaison]
  O --> C
  P --> C
  A --> B[10. Targeted bottleneck breaker]
  O --> B
  P --> B
  P --> I[9. Team integrator and submission author]
  E --> I
  C --> I
  B --> I
```

The foundation positions identify usable tools, candidate components, and hard
obstructions. The middle positions turn their handoffs into an architecture,
finite parameter ledger, proof lemmas, full-generator-matrix algorithm, and
one targeted attempt to break the current bottleneck. The cross-team liaison
imports compatible durable work. One integrator then consolidates the results
and writes a submission only when it is complete. Formal mathematical review
happens after a submission enters the independent verifier queue. Jobs cannot
begin until their displayed predecessors have completed.

Every position reads the shared repository and message board.  The dependency
edges create focus inside a team; they do not prevent importing a useful result
from another team.
