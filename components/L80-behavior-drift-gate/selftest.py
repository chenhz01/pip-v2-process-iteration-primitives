# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L80 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import behavior_fingerprint, gate

base = ["幂等性指同一操作执行多次与一次效果相同",
        "def bubble(a): ... 时间复杂度 O(n^2)",
        "本段主旨是……"]

# 断言① 指纹变化报警
fp1 = behavior_fingerprint(base)
drifted = base[:1] + ["冒泡排序大概就是两两交换吧"] + base[2:]
fp2 = behavior_fingerprint(drifted)
g1 = gate([fp1], fp2)
assert g1["verdict"] == "DRIFT-ALERT" and fp1 != fp2, g1

# 断言② 稳定不报（仅字面空白/大小写微调，规范化后指纹不变）
tweaked = ["幂等性指同一操作执行多次与一次效果相同 ",
           "DEF BUBBLE(a): ... 时间复杂度 O(n^2)",
           "本段主旨是……"]
fp3 = behavior_fingerprint(tweaked)
g2 = gate([fp1], fp3)
assert g2["verdict"] == "STABLE" and fp3 == fp1, g2

print("PASS")
sys.exit(0)
