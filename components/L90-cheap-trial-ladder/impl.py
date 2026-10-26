# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L90 廉价试错阶梯：校验试错序列成本单调性，'先贵后便宜' 拦截并建议重排。"""

DEFAULT_COSTS = {"doc_lookup": 0, "small_sample": 1, "pilot": 5, "full_rollout": 10}


def gate_trial_sequence(steps, costs=None):
    """steps: 试错动作序列；costs: 各动作成本表（默认免费->小额->全量）。

    成本必须非递减；出现回落 → 拦截，指出首个违规点并建议重排。
    """
    table = DEFAULT_COSTS if costs is None else costs
    seq = [(s, table[s]) for s in steps]
    for i in range(1, len(seq)):
        prev, cur = seq[i - 1], seq[i]
        if cur[1] < prev[1]:
            return {
                "verdict": "blocked",
                "at": i,
                "reason": (f"第 {i} 步 {cur[0]}(成本{cur[1]}) 比第 {i-1} 步 "
                           f"{prev[0]}(成本{prev[1]}) 还便宜：先贵后便宜，"
                           "试错顺序反了，建议按成本从低到高重排"),
                "sequence": seq,
            }
    return {"verdict": "ok", "at": None, "sequence": seq,
            "reason": "试错成本单调递增（从最便宜的试起），放行"}


if __name__ == "__main__":
    bad = ["full_rollout", "doc_lookup", "small_sample"]
    good = ["doc_lookup", "small_sample", "pilot", "full_rollout"]
    r1 = gate_trial_sequence(bad)
    print(f"[demo1] 判了什么: {r1['verdict']} | 为什么: {r1['reason']} | 数字: 违规位置=第 {r1['at']} 步")
    r2 = gate_trial_sequence(good)
    print(f"[demo2] 判了什么: {r2['verdict']} | 为什么: {r2['reason']}")
