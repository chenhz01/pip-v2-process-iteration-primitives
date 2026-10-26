# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L89 重放预演：用历史轨迹重放 N 个变体，最坏结局超承受线 → 建议不做或改方案。"""

import random


def replay_premortem(historical_outcomes, tolerance_line, n_variants=50,
                     jitter=0.1, seed=42):
    """historical_outcomes: 历史净结果（负值=亏损）；tolerance_line: 可承受下限。

    固定种子采样 N 个变体（历史值 ±jitter 扰动），输出结局分布与最坏情况。
    最坏 < 承受线 → 建议不做；否则放行。
    """
    rng = random.Random(seed)
    variants = [o * (1 + rng.uniform(-jitter, jitter))
                for o in rng.choices(historical_outcomes, k=n_variants)]
    worst = min(variants)
    best = max(variants)
    avg = sum(variants) / len(variants)
    below = sum(1 for v in variants if v < tolerance_line)
    if worst < tolerance_line:
        return {"verdict": "abort", "worst": round(worst, 2), "best": round(best, 2),
                "avg": round(avg, 2), "n_variants": n_variants, "below_line": below,
                "reason": (f"最坏结局 {worst:.2f} 超承受线 {tolerance_line}，"
                           f"变体中 {below}/{n_variants} 次破线，建议不做或改方案")}
    return {"verdict": "go", "worst": round(worst, 2), "best": round(best, 2),
            "avg": round(avg, 2), "n_variants": n_variants, "below_line": below,
            "reason": f"最坏结局 {worst:.2f} 在承受线 {tolerance_line} 内，分布可接受"}


if __name__ == "__main__":
    hist_risky = [-100.0, -40.0, 10.0, 30.0]
    hist_safe = [5.0, 8.0, 12.0, 20.0]
    r1 = replay_premortem(hist_risky, tolerance_line=-50.0)
    print(f"[demo1] 判了什么: {r1['verdict']} | 为什么: {r1['reason']} | "
          f"数字: 最坏={r1['worst']} 均值={r1['avg']} 破线={r1['below_line']}/{r1['n_variants']}")
    r2 = replay_premortem(hist_safe, tolerance_line=-50.0)
    print(f"[demo2] 判了什么: {r2['verdict']} | 为什么: {r2['reason']} | "
          f"数字: 最坏={r2['worst']} 均值={r2['avg']} 破线={r2['below_line']}/{r2['n_variants']}")
