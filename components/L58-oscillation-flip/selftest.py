# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L58 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import detect_oscillation

# 断言①：[x,y,x,y,x] 判振荡
hit, info = detect_oscillation(["x", "y", "x", "y", "x"])
assert hit is True, "断言①失败: %r" % info
assert info["verdict"] == "OSCILLATING" and info["period"] == 2, info

# 断言②：[x,x,x,y] 不判振荡
hit2, info2 = detect_oscillation(["x", "x", "x", "y"])
assert hit2 is False, "断言②失败: %r" % info2
assert info2["verdict"] == "STABLE", info2

# 负对照1：恒定结论 [x,x,x,x,x] 不是翻转
hit3, info3 = detect_oscillation(["x", "x", "x", "x", "x"])
assert hit3 is False, info3

# 负对照2：样本过短显式 SKIP，不硬判
hit4, info4 = detect_oscillation(["x", "y", "x"])
assert hit4 is False and info4["verdict"] == "SKIP", info4

print("PASS")
