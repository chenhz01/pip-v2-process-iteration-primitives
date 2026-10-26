# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L70 恢复成本估计 — 断点不是免费的：重算成本 vs 存档收益。

L1: 估计重算 token/时间成本，与存档收益（免重读/免重建上下文）比较，给「断/不断」建议。
L2: ①重算成本>存档收益时建议不断 ②反之建议断。
"""

TOKEN_COST = 0.002      # 每 token 重算成本（元）
TIME_WEIGHT = 0.05      # 每秒重算时间折价（元/秒）
BENEFIT_PER_KB = 0.5    # 每 KB 存档的恢复收益（免重读+免重建上下文）


def resume_estimate(recompute_tokens, recompute_seconds, checkpoint_kb):
    """比较「从存档接着干」的收益与「直接重算」的成本，给断/不断建议。"""
    if min(recompute_tokens, recompute_seconds, checkpoint_kb) < 0:
        raise ValueError("成本输入不得为负: %r" % ((recompute_tokens, recompute_seconds, checkpoint_kb),))
    recompute_cost = recompute_tokens * TOKEN_COST + recompute_seconds * TIME_WEIGHT
    benefit = checkpoint_kb * BENEFIT_PER_KB
    resume = benefit > recompute_cost
    return {"recompute_cost": round(recompute_cost, 4), "benefit": round(benefit, 4),
            "resume": resume,
            "advice": "断（用存档）" if resume else "不断（重算更划算）"}


def main():
    a = resume_estimate(recompute_tokens=50000, recompute_seconds=600, checkpoint_kb=20)
    b = resume_estimate(recompute_tokens=500, recompute_seconds=5, checkpoint_kb=200)
    print("场景A: 重算成本=%.2f 元 vs 存档收益=%.1f 元 → %s"
          % (a["recompute_cost"], a["benefit"], a["advice"]))
    print("场景B: 重算成本=%.4f 元 vs 存档收益=%.1f 元 → %s"
          % (b["recompute_cost"], b["benefit"], b["advice"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
