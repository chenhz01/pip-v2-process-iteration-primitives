# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L77 随机对照显著性 — 说自己有效？先跟瞎蒙的对照组比。

L1: 生成 N 个随机基线（固定种子），算目标成绩的百分位，<95 位 → 不显著。
L2: ①真提升判显著 ②随机水平判不显著。
"""

import random

N_CONTROLS = 256
SEED = 42
SIGNIFICANT_PCT = 95.0


def significance(target_mean, null_pool, n=N_CONTROLS, seed=SEED):
    """target_mean: 方法均值；null_pool: 瞎蒙水平的分数池。

    用固定种子从池中重采样生成 n 个随机对照，对目标做百分位排名。
    返回 {"percentile": float, "significant": bool, "n": n, "seed": seed}
    """
    if not null_pool:
        raise ValueError("null_pool 不能为空——没有对照就没有显著性")
    rng = random.Random(seed)
    baselines = [sum(rng.choice(null_pool) for _ in null_pool) / len(null_pool)
                 for _ in range(n)]
    pct = 100.0 * sum(1 for b in baselines if b < target_mean) / n
    return {"percentile": round(pct, 1), "significant": pct >= SIGNIFICANT_PCT,
            "n": n, "seed": seed}


def main():
    pool = [0.40, 0.45, 0.50, 0.55, 0.48, 0.52]
    strong = significance(0.90, pool)
    noise = significance(0.49, pool)
    print("真提升 target=0.90: 百分位=%.1f (N=%d, seed=%d) → %s"
          % (strong["percentile"], strong["n"], strong["seed"],
             "显著，结论成立" if strong["significant"] else "不显著"))
    print("随机水平 target=0.49: 百分位=%.1f → %s"
          % (noise["percentile"], "显著" if noise["significant"] else "不显著，跟瞎蒙没区别"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
