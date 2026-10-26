# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L73 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

TEAM = [
    {"name": "A", "status": "waiting", "waiting_seconds": 30, "blocked_chain": 3},
    {"name": "B", "status": "waiting", "waiting_seconds": 600, "blocked_chain": 1},
    {"name": "C", "status": "waiting", "waiting_seconds": 600, "blocked_chain": 3},
    {"name": "D", "status": "done", "waiting_seconds": 0, "blocked_chain": 0},
    {"name": "E", "status": "working", "waiting_seconds": 0, "blocked_chain": 0},
]

# 断言①: 被阻塞链最长的排最前（B 等得最久但链短，不得压过链长的 A/C）
r = impl.triage(TEAM)
assert r["queue"][0] in ("A", "C"), "链最长(3)应排最前，实际 %r" % r["queue"]
assert r["queue"].index("B") > r["queue"].index("A"), "链短的 B 不得排在链长的 A 前"

# 断言②: done 的不占队列
assert "D" not in r["queue"], "done 不应进队列"
assert r["excluded_done"] == ["D"], "done 应列入 excluded_done"
assert "E" not in r["queue"], "working 不应进队列"

# 断言③: 同链长时按等待时长排序（C 与 A 链相同，C 等更久排前）
assert r["queue"] == ["C", "A", "B"], "同链长比等待时长，实际 %r" % r["queue"]

# 负对照1: 全部 done → 空队列
z = impl.triage([{"name": "X", "status": "done", "waiting_seconds": 99, "blocked_chain": 9}])
assert z["queue"] == [], "全 done 应空队列"

# 负对照2: 非法输入要报错而非静默放行
try:
    impl.triage("bad")
    raise AssertionError("非列表输入应报 ValueError")
except ValueError:
    pass

print("PASS")
