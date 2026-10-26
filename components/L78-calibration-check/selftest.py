# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L78 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

# 断言①: 高置信低正确率报过信（0.9 置信却只有 25% 对）
over = impl.calibration_check([(0.9, False)] * 3 + [(0.9, True)] + [(0.85, False)] * 2)
assert over["overconfident"] is True, "高置信低正确率应报过信: %r" % over
assert over["ece"] > 0.15, "ECE=%.3f 应超阈" % over["ece"]
assert over["calibration_coef"] < 0.85, "校准系数应明显小于 1"

# 断言②: 校准良好不报
good = impl.calibration_check([(0.9, True)] * 9 + [(0.9, False)] +
                              [(0.5, True)] * 5 + [(0.5, False)] * 5)
assert good["overconfident"] is False, "说的把握≈真对的比例不应报: %r" % good
assert good["ece"] <= 0.15, "校准良好 ECE 应低于阈"

# 负对照1: 差距在阈内的高置信不算过信（0.85 置信 75% 对，差 0.10<0.15）
ok = impl.calibration_check([(0.85, True)] * 3 + [(0.85, False)])
assert ok["overconfident"] is False, "阈内偏差不应报过信: %r" % ok

# 负对照2: 空样本报错
try:
    impl.calibration_check([])
    raise AssertionError("空样本应报 ValueError")
except ValueError:
    pass

# 负对照3: 置信越界报错
try:
    impl.calibration_check([(1.5, True)])
    raise AssertionError("置信>1 应报 ValueError")
except ValueError:
    pass

print("PASS")
