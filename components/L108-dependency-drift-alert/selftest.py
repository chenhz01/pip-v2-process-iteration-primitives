# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L108 selftest — 对齐卡片 L2 两条断言。"""
import impl

OLD = {"requests": "2.31.0", "pydantic": "2.5.0", "numpy": "1.26.0"}
NEW = {"requests": "2.32.0", "pydantic": "2.5.0", "numpy": "2.0.0", "uvloop": "0.19.0"}

# 断言①：版本变更被列出（requests 升级、numpy 升级、uvloop 新增均须出现在差异中）
r1 = impl.diff_dependencies(OLD, NEW, critical={"numpy"})
assert r1["verdict"] == "ALERT", "存在依赖变更必须报警"
assert "requests" in r1["changed"] and r1["changed"]["requests"] == ["2.31.0", "2.32.0"], \
    "requests 版本变更必须被列出（含前后版本）"
assert "numpy" in r1["changed"] and "numpy" in r1["high_impact"], \
    "关键依赖 numpy 升级必须标高影响"
assert "uvloop" in r1["added"], "新增依赖必须被列出"
assert r1["old_hash"] != r1["new_hash"], "清单哈希应随内容变化"

# 断言②：无变化不报（QUIET、零差异、哈希一致）
r2 = impl.diff_dependencies(OLD, dict(OLD))
assert r2["verdict"] == "QUIET" and not (r2["added"] or r2["removed"] or r2["changed"]), \
    "无变化不得报警"
assert r2["old_hash"] == r2["new_hash"], "相同清单哈希必须一致"

# 负对照：删除依赖（numpy 被卸载）同样必须报警
r3 = impl.diff_dependencies(OLD, {"requests": "2.31.0", "pydantic": "2.5.0"})
assert r3["verdict"] == "ALERT" and "numpy" in r3["removed"], "依赖被删除必须报警"

print("PASS L108: 版本变更列出(断言①) / 无变化不报(断言②) / 删除依赖负对照 共4断言全过")
