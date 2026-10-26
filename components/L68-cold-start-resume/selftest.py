# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L68 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

# 断言①: 四项齐判 PASS
g = impl.cold_start_check({"goal": "g", "completed": "c", "next_step": "n", "constraints": "x"})
assert g["pass"] is True, "四项齐应判 PASS，实际 %r" % g

# 断言②: 缺「下一步」判 FAIL
b = impl.cold_start_check({"goal": "g", "completed": "c", "constraints": "x"})
assert b["pass"] is False, "缺 next_step 应判 FAIL"
assert "next_step" in b["missing"], "缺失清单应含 next_step，实际 %r" % b["missing"]

# 负对照1: 空串/纯空白字段视为缺失
e = impl.cold_start_check({"goal": "g", "completed": "  ", "next_step": "n", "constraints": "x"})
assert e["pass"] is False and "completed" in e["missing"], "空白字段应视为缺失"

# 负对照2: 非法输入（非 dict）判不合格而不是崩溃
x = impl.cold_start_check(None)
assert x["pass"] is False and len(x["missing"]) == 4, "非 dict 输入应判四项全缺"

print("PASS")
