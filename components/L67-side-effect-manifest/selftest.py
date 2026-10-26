# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L67 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import check

# 断言① 无清单拦截
r1 = check(None)
assert r1["verdict"] == "BLOCK" and "清单" in r1["reasons"][0], r1

# 断言② 清单含「不可逆」项时要求二次确认标记
m = [{"target": "prod-db.users", "reversibility": "irreversible", "impact": "全量用户表"},
     {"target": "draft.md", "reversibility": "reversible", "impact": "单文件"}]
r2a = check(m, actual_effects=("draft.md",), confirmed=False)
assert r2a["need_confirm"] is True and r2a["verdict"] == "BLOCK", r2a  # 未确认 → 拦
r2b = check(m, actual_effects=("draft.md",), confirmed=True)
assert r2b["verdict"] == "PASS" and r2b["need_confirm"] is True, r2b   # 已确认 → 放行

# 附加：实际触碰未声明的对象也要拦
r3 = check([{"target": "a.txt", "reversibility": "reversible", "impact": "单文件"}],
           actual_effects=("a.txt", "b.txt"))
assert r3["verdict"] == "BLOCK" and any("未声明" in x for x in r3["reasons"]), r3

print("PASS")
sys.exit(0)
