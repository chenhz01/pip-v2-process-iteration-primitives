# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L69 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

SNAP = {"dialog": ["u1", "a1"], "variables": {"n": 3}, "intermediates": [1, 2]}

# 断言①: 缺键报缺（intermediates 缺失 + variables 类型被改坏）
bad = impl.integrity_check(SNAP, {"dialog": ["u1"], "variables": "字符串"})
assert "intermediates" in bad["missing"], "缺键应出现在缺失清单，实际 %r" % bad["missing"]
assert not bad["pass"], "缺键+类型错应判 FAIL"
assert bad["type_mismatch"]["variables"] == ("dict", "str"), "类型不符应被定位"

# 断言②: 全齐报 PASS
ok = impl.integrity_check(SNAP, dict(SNAP))
assert ok["pass"] is True and ok["missing"] == [] and ok["type_mismatch"] == {}, "全齐应 PASS"

# 负对照1: 值类型漂移单独也能拦（键在但类型变了）
t = impl.integrity_check(SNAP, {"dialog": [], "variables": {}, "intermediates": {}})
assert not t["pass"] and "intermediates" in t["type_mismatch"], "list→dict 应报类型不符"

# 负对照2: 非法输入判 FAIL 而非崩溃
x = impl.integrity_check(SNAP, None)
assert x["pass"] is False, "restored=None 应判 FAIL"

print("PASS")
