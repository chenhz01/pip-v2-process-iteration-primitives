# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L81 selftest — 对齐卡片 L2 两条断言。"""
import sys
from impl import validate, validate_batch

# 断言① 缺原文引用判无效
bad = {"rule_id": "R-107", "fix": "补充来源标注"}
r1 = validate(bad)
assert r1["valid"] is False and r1["missing"] == ["quote"], r1

# 断言② 三件套齐判有效
good = {"rule_id": "R-102", "quote": "所有外发产物不得包含内部路径",
        "fix": "将内部路径替换为占位符后再发布"}
r2 = validate(good)
assert r2["valid"] is True and r2["missing"] == [], r2

# 附加：批量定位无效条目
rb = validate_batch([good, bad])
assert rb["all_valid"] is False and rb["invalid_indexes"] == [1], rb

print("PASS")
sys.exit(0)
