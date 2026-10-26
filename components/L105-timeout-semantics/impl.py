# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L105 超时语义 — 超时后它停了还是还在跑？分不清就重试，是事故之源。

L1：为每类调用标注超时语义（cancellable/uncancellable）；
    不可取消类超时后禁止盲重试（可能重复扣款/重复下单）；
    语义未登记的工具一律拦截（不清楚 = 不许赌）。
"""


def decide_retry(tool, registry, retries_done=0, max_retries=3):
    """超时后重试裁决。registry: tool -> 'cancellable' | 'uncancellable'。"""
    sem = registry.get(tool)
    if sem == "uncancellable":
        return {"verdict": "BLOCK", "semantics": "uncancellable",
                "reason": "不可取消：超时≠未执行，盲重试可能重复产生副作用（重试第%d次前被拦）" % (retries_done + 1)}
    if sem == "cancellable":
        if retries_done >= max_retries:
            return {"verdict": "BLOCK", "semantics": "cancellable",
                    "reason": "可取消但已达重试上限 %d 次" % max_retries}
        return {"verdict": "ALLOW", "semantics": "cancellable",
                "reason": "可取消：超时意味着已中止，重试安全（第%d/%d次）" % (retries_done + 1, max_retries)}
    return {"verdict": "BLOCK", "semantics": "unknown",
            "reason": "语义未登记：分不清停没停，禁止盲重试（先登记 cancellable/uncancellable）"}


if __name__ == "__main__":
    registry = {"http_get": "cancellable", "bank_transfer": "uncancellable"}
    r1 = decide_retry("http_get", registry)
    r2 = decide_retry("bank_transfer", registry)
    r3 = decide_retry("mystery_tool", registry)
    print("[1] http_get 超时      -> %s | %s" % (r1["verdict"], r1["reason"]))
    print("[2] bank_transfer 超时 -> %s | %s" % (r2["verdict"], r2["reason"]))
    print("[3] mystery_tool 超时  -> %s | %s" % (r3["verdict"], r3["reason"]))
    r4 = decide_retry("http_get", registry, retries_done=3)
    print("[4] 可取消但重试3次后  -> %s | %s" % (r4["verdict"], r4["reason"]))
