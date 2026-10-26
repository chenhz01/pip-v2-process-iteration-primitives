# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L66 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import record, verify

# 断言① 纯函数重放一致判 PASS
rec = record({"x": 7}, {"sq": 49})
r = verify(rec, {"x": 7}, {"sq": 49})
assert r["verdict"] == "PASS" and r["cause"] is None, r

# 断言② 含随机数未固定种子判 FAIL 并指出（输出侧漂移 = 非确定性来源）
rec2 = record({"x": 7}, {"sq": 49, "rand": 0.1111})      # 首跑采样
r2 = verify(rec2, {"x": 7}, {"sq": 49, "rand": 0.7777})  # 重放采样不同（模拟未固定种子）
assert r2["verdict"] == "FAIL", r2
assert r2["cause"] == "output-drift" and "随机" in r2["detail"], r2

print("PASS")
sys.exit(0)
