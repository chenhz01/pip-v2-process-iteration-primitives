# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L75 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

BASE = [3.0, 3.1, 2.9, 3.0, 3.0, 3.1, 2.9, 3.0]

# 断言①: 分数整体上移 >2σ 报漂移
loose = impl.drift_gate(BASE, [3.6, 3.7, 3.8, 3.7])
assert loose["drift"] is True, "上移约 9.9σ 应报漂移"
assert loose["mean_shift_sigma"] > 2.0, "σ 漂移应 >2，实际 %r" % loose["mean_shift_sigma"]
assert any("均值" in r for r in loose["reasons"]), "理由应含均值漂移"

# 断言②: 平稳不报
stable = impl.drift_gate(BASE, [3.0, 3.1, 3.0, 2.9])
assert stable["drift"] is False, "平稳序列不应报漂移: %r" % stable

# 负对照1: 小幅波动 (<2σ) 不报
small = impl.drift_gate(BASE, [3.05, 3.1, 3.05, 3.1])
assert small["drift"] is False, "约 1σ 的波动不应报漂移"

# 负对照2: 方差膨胀单独也能触发（均值没动但忽高忽低）
wild = impl.drift_gate(BASE, [1.0, 5.0, 1.5, 4.5])
assert wild["drift"] is True and wild["var_ratio"] > 4.0, "方差膨胀应触发"

# 负对照3: 样本不足要报错而非硬算
try:
    impl.drift_gate(BASE, [3.0])
    raise AssertionError("样本不足应报 ValueError")
except ValueError:
    pass

print("PASS")
