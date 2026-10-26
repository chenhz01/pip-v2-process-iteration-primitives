# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L86 selftest：对齐卡片 L2 断言 ①旧低信记忆排后 ②高信新记忆排前。"""

from impl import rank_memories, credit_score

mems = [
    {"id": "old_low", "credit": 0.2, "age_days": 365},
    {"id": "new_high", "credit": 0.9, "age_days": 1},
    {"id": "mid", "credit": 0.5, "age_days": 30},
]
ranked = rank_memories(mems)
order = [e["id"] for e, _ in ranked]

# 断言②：高信新记忆排前
assert order[0] == "new_high", f"高信新记忆应排第一, got {order}"
# 断言①：旧低信记忆排后
assert order[-1] == "old_low", f"旧低信记忆应排最后, got {order}"
# 低分条目仍在结果中：降权不删除
assert len(ranked) == 3, "降权不是删除"
# 时间衰减单调性：同信用，越老分越低
assert credit_score({"credit": 1.0, "age_days": 10}, 30) > \
       credit_score({"credit": 1.0, "age_days": 100}, 30)

print("PASS")
