# PIP-2.0 · Process Iteration Primitives (generation 2)

**55 zero-dependency primitives for the health of the loop itself: when it cannot stop, when its tools mean nothing, when its conclusions cannot be killed.**

[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE) [![Spec: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)

---

## The problem

PIP-1.0 decided **when an iteration should stop**. This set looks one layer down — at the loop itself, at the tools it calls, and at the honesty of what it reports:

1. **The loop is sick, not slow.** It is livelocked, waiting on itself, or oscillating between two answers. Every metric still says 'working'.
2. **The tools answer, but their answers have no semantics.** Fresh? Stale? Timed out? Retryable?
3. **Nobody audits the auditor.** The judge that gates every step drifts, and the evaluation itself now costs several times what the agent costs.
4. **Conclusions are not falsifiable.** No source for the numbers, no counterexample required, no condition under which the claim would die.

`PIP-2.0` ships **55 primitives** (2469 lines of Python in total). Each is **30–80 lines, standard library only, embeddable in any loop**.

It is not a framework. It is a toolbox — take the wrench you need.

---

## What is in here

| Cluster | What it protects you from | Primitives |
|---|---|---|
| **Cognitive Honesty** | Numbers with no source, claims with no counterexample, conclusions no evidence could kill. | 4 |
| **Tool Semantics** | The tool works. Was it fresh? Did it time out or return stale? Nobody checks. | 4 |
| **Dependencies & Environment** | It worked yesterday on this machine. Today nothing changed, except everything. | 3 |
| **Loop Pathology** | The loop is not converging but nothing is failing — livelock, deadlock, oscillation. All three look like 'working'. | 4 |
| **Sampling & Triage** | Evaluation now costs more than the agent itself. Cheap filtering first, expensive diagnosis second. | 4 |
| **Idempotency & Replay** | You cannot retry safely if you do not know whether the first attempt committed anything. | 4 |
| **Checkpoint & Resume** | A checkpoint without intent and plan cannot be resumed by someone who was not there. | 4 |
| **Agent-to-Agent Handoff** | Agent A hands to agent B and B starts over, because the protocol carried output but not state. | 3 |
| **Judge Health** | The judge that guards every step is itself drifting, and nobody audits the judge. | 4 |
| **Prompt Regression** | The prompt changed. Behaviour changed. No diff, no test, no idea which change did it. | 3 |
| **Context Economics** | Pruning the middle invalidates the prefix cache — everyone wants to do it, everyone gives up. | 3 |
| **Memory Write Gate** | Old memory is overwritten rather than deleted, and the model just picks the nearest one. | 3 |
| **Pre-flight Admission** | Stop-loss must be set before entering the trade, not after losing money. | 3 |
| **Repair Companion** | Every bug fix should ship with the detector that would have caught it. | 3 |
| **Undo & Blast Radius** | 'We can roll back' means little if there are three rollback paths and none was ever exercised. | 3 |
| **Determinism Division** | Half the steps should be code, not tokens. Nobody asks which. | 3 |
| | **total** | **55** |

<sub>Learning cards in `cards/CARDS.md` are written in Chinese (plain-language → mechanism → how to use → when it fails). Code, identifiers and this README are English.</sub>

---

## Quick start

```bash
python components/L100-unsourced-number-gate/impl.py      # what it does, on built-in demo data
python components/L100-unsourced-number-gate/selftest.py  # hard assertions that it does that
python run_all.py                 # every component, own process each
```

```python
import sys; sys.path.insert(0, 'components/L100-unsourced-number-gate')
from impl import *                # then call it from your own loop
```

---

## What has been verified, and what has not

| Check | Result | Note |
|---|---|---|
| Runs in its own process | **55/55** | both `selftest.py` and `impl.py`, fresh interpreter each |
| Third-party dependencies | **0** | stdlib only, by construction |
| Determinism | enforced in-repo | no network, no randomness; seeded where unavoidable |
| Explicit bad-input contract | **partial** | not every primitive validates its inputs explicitly; some rely on native exceptions. We did not add no-op guards just to satisfy a checker |
| Real-world adoption | **none yet** | these are new; no production usage is claimed |

**Honest limits.** Each primitive decides from structured data you must supply — scores, events, manifests, calls. It cannot judge whether a design is good, whether prose has a voice, or whether a judgement about people is fair. Forcing it into those questions produces confident nonsense.

---

## License and attribution

Dual-licensed:

- **Code** — Apache License 2.0. See [LICENSE](LICENSE).
- **Specification & docs** — Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE-SPEC](LICENSE-SPEC).

If you publicly claim that your implementation **conforms to / passes / implements PIP-2.0**, you must attribute: `PIP-2.0 · pip-v2-process-iteration-primitives © 2026 chenhz01, CC BY 4.0` plus the spec link https://github.com/chenhz01/pip-v2-process-iteration-primitives.

If you make no such claim, use it freely — commercial, closed-source, renamed, no attribution needed.

---

## Where these came from

`docs/GAP_PROBE.md` records the sampled GitHub search behind this set, including the three neighbourhoods abandoned as overcrowded. `docs/V1_V2_COMPARISON.md` maps every v2 cluster against the nearest v1 cluster and states why each pair is not a duplicate.

