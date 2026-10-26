# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L79 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import check

snap = {"input": "用 Python 写快排",
        "expected": {"lang_zh": True, "has_code": True, "has_list": False}}

# 断言① 关键特征漂移报回归（语言翻成英文 = 关键特征漂移）
r1 = check(snap, "Sure, here is quicksort:\n```python\ndef qs(a): ...\n```")
assert r1["verdict"] == "REGRESSION", r1
assert "lang_zh" in r1["drift"], r1

# 断言② 一致放行（字面微调、结构特征一致）
r2 = check(snap, "好的，这是快排：\n```python\ndef qs(a): ...\n```\n欢迎追问。")
assert r2["verdict"] == "PASS" and r2["drift"] == {}, r2

print("PASS")
sys.exit(0)
