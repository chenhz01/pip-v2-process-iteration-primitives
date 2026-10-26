# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L70 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

# 断言①: 重算成本 > 存档收益 → 建议不断
a = impl.resume_estimate(recompute_tokens=500, recompute_seconds=5, checkpoint_kb=2)
# 重算成本 = 500*0.002 + 5*0.05 = 1.25 元；收益 = 2*0.5 = 1.0 元
assert a["recompute_cost"] > a["benefit"], "构造应满足重算成本>收益: %r" % a
assert a["resume"] is False and "不断" in a["advice"], "重算更划算应建议不断: %r" % a

# 断言②: 重算成本 < 存档收益 → 建议断（从存档接着干更划算）
b = impl.resume_estimate(recompute_tokens=100000, recompute_seconds=3600, checkpoint_kb=1000)
# 重算成本 = 200+180 = 380 元；收益 = 1000*0.5 = 500 元 → 500>380 应建议断
assert b["recompute_cost"] < b["benefit"] and b["resume"] is True, "存档更划算应建议断: %r" % b
assert "断" in b["advice"], "advice 应含『断（用存档）』"

# 负对照1: 成本与收益相等 → 严格大于才断，相等不算；重算成本>收益 → 不断
c = impl.resume_estimate(recompute_tokens=250, recompute_seconds=10, checkpoint_kb=1)
# 0.5+0.5=1.0 vs 0.5*1=0.5 → 重算成本>收益 → 建议不断
assert c["resume"] is False, "重算成本>收益应建议不断: %r" % c
d = impl.resume_estimate(recompute_tokens=500, recompute_seconds=0, checkpoint_kb=2)
# 1.0 vs 1.0 相等 → 不建议断（严格大于）
assert d["resume"] is False, "成本==收益应保守判不断"

# 负对照2: 负数/非法输入应被拦（成本非负约束）
try:
    impl.resume_estimate(-1, 0, 0)
    raise AssertionError("负 token 应被拒绝")
except ValueError:
    pass

print("PASS")
