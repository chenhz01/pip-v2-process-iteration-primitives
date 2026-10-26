# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L83 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import assess, estimate_coverage

# 断言① 超上阈报压缩
r1 = assess(1.0)
assert r1["verdict"] == "OVERFLOW" and "压缩" in r1["action"], r1

# 断言② 低于下阈报补料
c2 = estimate_coverage("只有一句寒暄，没有实质内容", ["预算", "截止日期", "负责人"])
assert abs(c2 - 0.0) < 1e-9, c2
r2 = assess(c2)
assert r2["verdict"] == "INSUFFICIENT" and "补料" in r2["action"], r2

# 附加：居中区间维持
r3 = assess(0.5)
assert r3["verdict"] == "OK", r3

print("PASS")
sys.exit(0)
