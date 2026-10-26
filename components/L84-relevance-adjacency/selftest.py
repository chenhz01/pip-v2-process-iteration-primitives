# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L84 selftest：对齐卡片 L2 断言 ①高分散建议重组 ②集中不报。"""

from impl import relevance_adjacency

# 断言①：头 2、尾 97，分散度 0.95 > 0.5 → 建议重组
a = relevance_adjacency(100, [2, 3, 97])
assert a["verdict"] == "reorganize", f"高分散应建议重组, got {a}"
assert a["dispersion"] > 0.5, f"分散度应超阈, got {a['dispersion']}"

# 断言②：三块集中在 10~15，分散度 0.05 → 不报
b = relevance_adjacency(100, [10, 12, 15])
assert b["verdict"] == "ok", f"集中应不报, got {b}"
assert b["dispersion"] <= 0.5, f"分散度应低于阈值, got {b['dispersion']}"

# 边界：不足两块不误报
assert relevance_adjacency(100, [50])["verdict"] == "ok"

print("PASS")
