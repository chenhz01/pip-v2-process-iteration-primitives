# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L60 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import decide, pick_gear

# 断言①：可逆 + 低影响 -> cheap
r1 = decide({"reversible": True, "blast_radius": 1, "failure_rate": 0.1})
assert r1["gear"] == "cheap", "断言①失败: %r" % r1

# 断言②：不可逆 + 高影响 -> max
r2 = decide({"reversible": False, "blast_radius": 5, "failure_rate": 0.2})
assert r2["gear"] == "max", "断言②失败: %r" % r2

# 负对照1：高失败率的可逆步骤不许进 cheap，应落 balanced
r3 = decide({"reversible": True, "blast_radius": 1, "failure_rate": 0.5})
assert r3["gear"] == "balanced", r3

# 负对照2：档位只能三选一，且理由非空
for rev, br in [(True, 3), (False, 1), (True, 2)]:
    g, why = pick_gear(rev, br, 0.1)
    assert g in ("cheap", "balanced", "max") and why, (g, why)

print("PASS")
