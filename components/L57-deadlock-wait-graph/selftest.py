# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L57 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import find_deadlock, check_agents

# 断言①：A等B、B等A -> 判死锁
hit, info = check_agents({"A": {"waiting_on": "B"},
                          "B": {"waiting_on": "A"}})
assert hit is True, "断言①失败: %r" % info
assert info["verdict"] == "DEADLOCK" and sorted(info["cycle"]) == ["A", "B"], info

# 断言②：A等B、B在跑 -> 不判死锁
hit2, info2 = check_agents({"A": {"waiting_on": "B"},
                            "B": {"waiting_on": None}})
assert hit2 is False, "断言②失败: %r" % info2
assert info2["verdict"] == "OK", info2

# 负对照1：三节点链式等待不成环
hit3, _ = find_deadlock({"A": "B", "B": "C", "C": None})
assert hit3 is False

# 负对照2：自等（A等A）也是一元环，必须报死锁
hit4, cyc = find_deadlock({"A": "A", "B": None})
assert hit4 is True and cyc == ["A"], (hit4, cyc)

print("PASS")
