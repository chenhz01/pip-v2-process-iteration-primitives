# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L82 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import evaluate

segs = [{"id": f"s{i}", "tokens": t} for i, t in enumerate([200, 100, 200, 200, 200])]

# 断言① 中部删除负收益被否（省 100 vs 其后 600 token 全部重算赔 1200）
r1 = evaluate(segs, 1)
assert r1["verdict"] == "VETO" and r1["net"] < 0, r1
assert r1["suggestion"] and "尾部" in r1["suggestion"], r1

# 断言② 尾部删除正收益放行（其后 0 token，无重算成本）
r2 = evaluate(segs, 4)
assert r2["verdict"] == "APPROVE" and r2["net"] > 0, r2
assert r2["tokens_after"] == 0, r2

print("PASS")
sys.exit(0)
