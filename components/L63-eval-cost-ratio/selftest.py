# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L63 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import eval_cost_ratio

# 断言①：5.0 倍 -> 报警且给三条降本路径
r1 = eval_cost_ratio(500.0, 100.0)
assert r1["alarm"] is True, "断言①失败: %r" % r1
assert abs(r1["ratio"] - 5.0) < 1e-9, r1
assert len(r1["paths"]) == 3, "报警时应给三条降本路径: %r" % r1["paths"]

# 断言②：0.5 倍 -> 不报
r2 = eval_cost_ratio(50.0, 100.0)
assert r2["alarm"] is False, "断言②失败: %r" % r2
assert r2["paths"] == [], r2

# 负对照1：work_cost 非正 -> 显式报错，不静默
try:
    eval_cost_ratio(10.0, 0)
except ValueError:
    pass
else:
    raise AssertionError("work_cost=0 应显式报错")

# 负对照2：比值恰等于阈值（3.0）不算超阈，不报警
r3 = eval_cost_ratio(300.0, 100.0, alarm_threshold=3.0)
assert r3["alarm"] is False, r3

print("PASS")
