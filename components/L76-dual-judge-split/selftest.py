# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L76 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

A = {"正确性": 9, "完整性": 8, "风格": 7}

# 断言①: 分差超阈触发仲裁，并定位分歧维度
bad = impl.split_check(A, {"正确性": 9, "完整性": 4, "风格": 7})
assert bad["arbitrate"] is True, "完整性分差 4>2 应触发仲裁"
assert bad["agree"] is False, "分歧情形不应 agree"
assert bad["dimensions"]["完整性"]["flag"] is True, "分歧维度应被定位"
assert bad["dimensions"]["正确性"]["flag"] is False, "一致维度不应误标"

# 断言②: 一致直接过
ok = impl.split_check(A, {"正确性": 9, "完整性": 8, "风格": 8})
assert ok["arbitrate"] is False and ok["agree"] is True, "一致应直接过"

# 负对照1: 分差恰好等于阈值（2.0）不触发（严格大于）
edge = impl.split_check({"x": 7}, {"x": 9})
assert edge["arbitrate"] is False, "分差==2.0 不应触发"

# 负对照2: 维度集不一致要报错，不许静默比
try:
    impl.split_check({"x": 1}, {"y": 1})
    raise AssertionError("维度不一致应报 ValueError")
except ValueError:
    pass

# 负对照3: 非字典输入报错
try:
    impl.split_check([1, 2], [1, 2])
    raise AssertionError("非字典应报 ValueError")
except ValueError:
    pass

print("PASS")
