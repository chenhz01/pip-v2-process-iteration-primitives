# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L77 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

POOL = [0.40, 0.45, 0.50, 0.55, 0.48, 0.52]  # 瞎蒙水平，均值≈0.483

# 断言①: 真提升判显著（远超随机对照第 95 位）
strong = impl.significance(0.90, POOL)
assert strong["significant"] is True, "target=0.90 应显著: %r" % strong
assert strong["percentile"] >= 95.0, "百分位应 ≥95，实际 %r" % strong["percentile"]
assert strong["n"] == 256 and strong["seed"] == 42, "应对 256 个固定种子对照排名"

# 断言②: 随机水平判不显著
noise = impl.significance(0.49, POOL)
assert noise["significant"] is False, "target≈瞎蒙水平不应显著: %r" % noise
assert noise["percentile"] < 95.0, "随机水平百分位应 <95"

# 负对照1: 同参数两次调用结果必须一致（固定种子，可复现）
r1 = impl.significance(0.49, POOL)
r2 = impl.significance(0.49, POOL)
assert r1["percentile"] == r2["percentile"], "固定种子下必须可复现"

# 负对照2: 空对照池要报错——没有对照就没有显著性
try:
    impl.significance(0.9, [])
    raise AssertionError("空对照池应报 ValueError")
except ValueError:
    pass

# 负对照3: 目标低于对照均值 → 百分位应很低
low = impl.significance(0.30, POOL)
assert low["percentile"] <= 5.0, "低于瞎蒙水平应排末位: %r" % low

print("PASS")
