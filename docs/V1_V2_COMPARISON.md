# PIP-1.0 vs PIP-2.0 — what changed, and what did not duplicate

PIP-1.0 answered **"should this iteration stop?"**
PIP-2.0 answers **"is the loop itself healthy, are the tools honest, and is the conclusion honest?"**

## Cluster-level mapping

| v2 cluster | count | nearest v1 cluster | relation | note |
|---|---|---|---|---|
| Loop Pathology | 4 | — (v1 only decides *whether* to stop) | new | v1 judges convergence; v2 diagnoses *cannot stop* |
| Sampling & Triage | 4 | — | new | evaluation costs more than the agent itself |
| Idempotency & Replay | 4 | — | new | replay equivalence made decidable |
| Checkpoint & Resume | 4 | — | new | resume requires intent + plan, not just state |
| Agent-to-Agent Handoff | 3 | Human Handoff (v1, content layer) | orthogonal | v1 = when a human takes over; v2 = protocol between agents |
| Judge Health | 4 | Silent Failure (v1, adjacent) | orthogonal | v1 catches "failed silently"; v2 catches "the judge drifted" |
| Prompt Regression | 3 | — | new | snapshot diff + behaviour drift gate |
| Context Economics | 3 | Context Hygiene (v1) | extends | v1 decides *what* to drop; v2 prices the drop |
| Memory Write Gate | 3 | — | new | contradiction / decay / stale-reference checks |
| Pre-flight Admission | 3 | Completion Definition (v1) | extends | v1 checks after the fact; v2 refuses to start |
| Repair Companion | 3 | — | new | every fix ships with its detector |
| Undo & Blast Radius | 3 | Rollback Readiness (v1) | extends | v1 asks "is there a snapshot"; v2 asks "is there exactly one path, exercised" |
| Determinism Division | 3 | — | new | code vs token, decided per step |
| Cognitive Honesty | 4 | (none) | asset promoted | unsourced numbers, absolutisation, forcing negative controls |
| Tool Semantics | 4 | Tool Self-test (v1) | extends | v1 tests *does it work*; v2 tests *what does the result mean* |
| Dependencies & Environment | 3 | — | new | the machine changed underneath you |

**Totals: 9 new + 4 extends + 2 orthogonal + 1 promoted = 16 clusters.** Generations combined: 30 clusters, 110 primitives.

## Pairwise dedup (the rule we used)

| v2 primitive | nearest v1 primitive | why it is not a duplicate |
|---|---|---|
| Cache-aware Pruning | Context Hygiene / Trace Minimisation | v1 owns *what* to delete; v2 owns the *cost* of deleting (cache recompute) |
| Undo Uniqueness Test | Rollback Readiness | v1 checks existence of a snapshot; v2 checks uniqueness and that it was exercised |
| Exit Criteria First | Completion Definition Check | v1 is in-flight inspection; v2 is pre-flight admission |
| Evaluation Cost Ratio | Cost per Insight | different denominators: eval vs agent, insight vs token |
| Attention Triage | Interruption Cost | v1 prices one interruption; v2 schedules across agents |
| Absolutisation Red Light | (no v1 counterpart) | promoted from an internal judging aid, not a repeat |
| Tool Semantics cluster | Tool Self-test | v1 checks function; v2 checks meaning |

**Rejected outright:** an earlier "silent failure detection" candidate (duplicated v1), and three overcrowded
neighbourhoods (`agent regression guard`, `claim verification`, `prompt versioning`).
