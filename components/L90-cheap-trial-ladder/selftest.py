# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L90 selftest：对齐卡片 L2 断言 ①全量先行拦截 ②阶梯正确放行。"""

from impl import gate_trial_sequence

# 断言①：全量打头，后面却去查文档 → 拦截并指出违规点
r1 = gate_trial_sequence(["full_rollout", "doc_lookup", "small_sample"])
assert r1["verdict"] == "blocked", f"全量先行应拦截, got {r1}"
assert r1["at"] == 1, f"首个违规点应为第 1 步(0 基), got {r1['at']}"

# 断言②：免费 -> 小样 -> 全量，成本单调递增 → 放行
r2 = gate_trial_sequence(["doc_lookup", "small_sample", "full_rollout"])
assert r2["verdict"] == "ok", f"阶梯正确应放行, got {r2}"

# 平级成本（非递减）不算违规
r3 = gate_trial_sequence(["doc_lookup", "doc_lookup", "full_rollout"])
assert r3["verdict"] == "ok"

# 自定义成本表同样生效
r4 = gate_trial_sequence(["expensive", "cheap"], costs={"expensive": 9, "cheap": 1})
assert r4["verdict"] == "blocked"

print("PASS")
