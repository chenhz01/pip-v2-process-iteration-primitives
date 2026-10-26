# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L109 selftest — 对齐卡片 L2 两条断言。"""
import impl

SAVED = {"platform": "win32", "python": "3.13.12", "workdir": "C:/proj", "deps_hash": "a1b2c3"}

# 断言①：指纹不符要求确认（Python 升级 → CONFIRM 且指出差异项）
r1 = impl.compare_env(SAVED, dict(SAVED, python="3.14.0"))
assert r1["verdict"] == "CONFIRM", "指纹不符必须要求确认而非直接恢复"
assert r1["mismatched"] == ["python"], "必须定位到不一致的具体指纹项"

# 断言②：一致直接恢复（RESUME、零差异）
r2 = impl.compare_env(SAVED, dict(SAVED))
assert r2["verdict"] == "RESUME" and not r2["mismatched"], "指纹一致应直接恢复"

# 负对照①：缺指纹项比不一致更危险 → REBUILD（不许硬跑）
r3 = impl.compare_env(SAVED, {"platform": "win32", "python": "3.13.12"})
assert r3["verdict"] == "REBUILD" and "deps_hash" in r3["missing"], "缺指纹项必须要求重建"

# 负对照②：多出未知项同样不可直接恢复
r4 = impl.compare_env(SAVED, dict(SAVED, extra_pkg="ghost"))
assert r4["verdict"] == "CONFIRM" and "extra_pkg" in r4["extra"], "环境多出未知项也要求确认"

print("PASS L109: 不符要求确认(断言①) / 一致直接恢复(断言②) / 缺项REBUILD+多出项负对照 共4断言全过")
