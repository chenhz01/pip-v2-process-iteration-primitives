# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L56 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import detect_livelock

# 断言①：对 [A,B,A,B,A,B] 判活锁
hit, info = detect_livelock(["A", "B", "A", "B", "A", "B"], new_facts=[])
assert hit is True, "断言①失败: %r" % info
assert info["verdict"] == "LIVELOCK", info

# 断言②：对带新产物的 [A,B,C] 判正常
hit2, info2 = detect_livelock(["A", "B", "C"], new_facts=["artifact_1"])
assert hit2 is False, "断言②失败: %r" % info2
assert info2["verdict"] == "NORMAL", info2

# 负对照1：过短序列必须显式 SKIP，不许误判
hit3, info3 = detect_livelock(["A"])
assert hit3 is False and info3["verdict"] == "SKIP", info3

# 负对照2：动作重复但有新事实产出，不判活锁
hit4, _ = detect_livelock(["A", "B", "A", "B"], new_facts=["f1", "f2"])
assert hit4 is False

print("PASS")
