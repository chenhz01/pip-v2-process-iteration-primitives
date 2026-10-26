# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L104 selftest — 对齐卡片 L2 两条断言。"""
import impl

CACHED = {"name": "pay", "params": {"amount": "num"}, "returns": ["ok"]}
DRIFTED = {"name": "pay", "params": {"amount_cents": "num"}, "returns": ["ok", "txn_id"]}
CALLS = [{"name": "下单支付", "tool": "pay"}]

# 断言①：schema 变化被列出（参数改名 + 返回新增字段均出现在差异清单中，判 BLOCK）
r1 = impl.check_contract_drift(CACHED, DRIFTED, CALLS)
assert r1["verdict"] == "BLOCK" and r1["drift"] is True, "漂移应判 BLOCK"
assert any("params.amount" in d for d in r1["diffs"]), "参数改名必须被列出"
assert any("returns.txn_id" in d for d in r1["diffs"]), "返回新增字段必须被列出"
assert r1["affected_calls"] == ["下单支付"], "受影响调用点应被标记"

# 断言②：一致放行（零差异、PASS）
r2 = impl.check_contract_drift(CACHED, CACHED, CALLS)
assert r2["verdict"] == "PASS" and r2["diffs"] == [], "一致应放行且零差异"

# 负对照：仅键顺序不同（JSON 键序无语义）不得误报为漂移
r3 = impl.check_contract_drift(
    {"params": {"a": "int"}, "name": "t", "returns": ["x"]},
    {"name": "t", "returns": ["x"], "params": {"a": "int"}})
assert r3["verdict"] == "PASS", "键顺序不同不应判漂移（规范化失效）"

print("PASS L104: 漂移列出+调用点标记(断言①) / 一致放行(断言②) / 键序负对照 共5断言全过")
