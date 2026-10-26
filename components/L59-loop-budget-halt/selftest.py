# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L59 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import loop_budget_halt

# 断言①：5 步无新信息且花费超阈 -> 返回 HALT
h1, i1 = loop_budget_halt(5, 12.0, cost_limit=10.0, no_info_limit=5)
assert h1 is True, "断言①失败: %r" % i1
assert i1["signal"] == "HALT", i1

# 断言②：有新信息（无新信息步数为 0）且花费未超阈 -> 不返回 HALT
h2, i2 = loop_budget_halt(0, 4.0, cost_limit=10.0, no_info_limit=5)
assert h2 is False, "断言②失败: %r" % i2
assert i2["signal"] == "CONTINUE", i2

# 负对照1：花费超阈但步数未超 -> 仍 HALT（任一超阈即停，验证另一条线）
h3, i3 = loop_budget_halt(2, 11.0, cost_limit=10.0, no_info_limit=5)
assert h3 is True and i3["over_cost"] is True and i3["over_stall"] is False, i3

# 负对照2：步数刚好差一步不到限 -> 不熔断
h4, i4 = loop_budget_halt(4, 4.0, cost_limit=10.0, no_info_limit=5)
assert h4 is False, i4

print("PASS")
