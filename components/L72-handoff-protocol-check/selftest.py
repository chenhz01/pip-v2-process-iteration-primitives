# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L72 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

GOOD = {"status": "阶段A完成", "blockers": [], "next_step": "B 接手 API 层",
        "permission_boundary": "只许写 api/"}

# 断言①: 缺「阻塞项」拒收
b = impl.handoff_check({k: v for k, v in GOOD.items() if k != "blockers"})
assert b["accept"] is False, "缺阻塞项应拒收"
assert "blockers" in b["missing"], "缺失清单应含 blockers"

# 断言②: 齐全签收（空列表的 blockers 也算写全了——明确无阻塞）
g = impl.handoff_check(GOOD)
assert g["accept"] is True, "齐全应签收，实际 %r" % g

# 负对照1: blockers 是空串也不算写全
s = impl.handoff_check(dict(GOOD, blockers="   "))
assert s["accept"] is False and "blockers" in s["missing"], "空白阻塞项应拒收"

# 负对照2: 一次缺多项要全列出来
m = impl.handoff_check({"status": "x"})
assert set(m["missing"]) == {"blockers", "next_step", "permission_boundary"}, "应列出全部缺项"

# 负对照3: 非法输入拒收
assert impl.handoff_check(None)["accept"] is False

print("PASS")
