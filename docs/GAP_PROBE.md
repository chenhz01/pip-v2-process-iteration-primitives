# Where these came from — a sampled GitHub search

Method: GitHub repo search, **≤3 content terms per query** (longer queries collapse to ~0 results and
produce a false "empty field"), each thin result re-checked with one term removed, and the top-3 hits
opened to confirm they actually do the thing.

| neighbourhood | query | repos found | reading |
|---|---|---|---|
| loop pathology | `agent loop deadlock` | 11 | empty — top 2 hits are copies of each other |
| sampling policy | `adaptive temperature llm` | 6 | very thin (the 0-result version was query collapse) |
| idempotency | `tool call idempotency` | 46 | emerging — every repo had 0 stars |
| judge drift | `judge drift llm` | 130 | half-empty — well-matched hits were ≤3 stars |
| checkpoint resume | `agent checkpoint resume` | 225 | half-full, few well-matched |
| handoff protocol | `agent handoff protocol` | 236 | half-full, protocol layer thin |
| prompt regression | `prompt regression testing` | 487 | half-full, all early-stage (≤17 stars) |
| memory decay | `agent memory decay` | 298 | filling up |

**Deliberately abandoned as overcrowded:** `agent regression guard` (2310 repos, two thousand-star
occupants), `claim verification` (6421), `prompt versioning` (2874).

**What this evidence does and does not say.** 16 neighbourhoods were sampled. It shows the sampled
neighbourhoods are thin. It does **not** establish that nothing like these primitives exists anywhere,
and no priority or novelty claim is made.
