# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L89 selftest：对齐卡片 L2 断言 ①最坏超线建议不做 ②分布可接受放行。"""

from impl import replay_premortem

# 断言①：历史含 -100 的大亏，承受线 -50 → 最坏必破线，建议不做
r1 = replay_premortem([-100.0, -40.0, 10.0, 30.0], tolerance_line=-50.0, seed=42)
assert r1["verdict"] == "abort", f"最坏超线应建议不做, got {r1}"
assert r1["worst"] < -50.0, f"最坏值应低于承受线, got {r1['worst']}"
assert r1["n_variants"] == 50, "应重放 50 个变体"

# 断言②：历史全为正收益，承受线 -50 → 放行
r2 = replay_premortem([5.0, 8.0, 12.0, 20.0], tolerance_line=-50.0, seed=42)
assert r2["verdict"] == "go", f"分布可接受应放行, got {r2}"
assert r2["worst"] >= -50.0, f"最坏值不应破线, got {r2['worst']}"

# 确定性：同种子同输入重放结果一致
assert r2 == replay_premortem([5.0, 8.0, 12.0, 20.0], tolerance_line=-50.0, seed=42)

print("PASS")
