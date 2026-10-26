# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L92 selftest：断言对齐卡片 L2（①测试未迁移拦截 ②迁移且通过放行）。"""

import sys

from impl import check_port_readiness


def main():
    # L2-1 测试未迁移 → 拦截
    ok1, d1 = check_port_readiness({"target": "py3.13", "tests": {"migrated": False}})
    assert not ok1, "L2-1 失败：测试未迁移应拦截"
    assert "未迁移" in d1["reason"]

    # L2-2 迁移且通过 → 放行
    ok2, d2 = check_port_readiness({
        "target": "py3.13", "tests": {"migrated": True, "total": 40, "passed": 40}})
    assert ok2, "L2-2 失败：迁移且全过应放行"
    assert d2["pass_rate"] == 1.0

    # 负对照：通过率不足、计数造假、坏输入都要拦
    ok3, d3 = check_port_readiness({
        "target": "py3.13", "tests": {"migrated": True, "total": 40, "passed": 37}})
    assert not ok3 and d3["pass_rate"] == 0.925, "通过率 37/40 未达标线应拦"
    ok4, _ = check_port_readiness({
        "target": "py3.13", "tests": {"migrated": True, "total": 5, "passed": 9}})
    assert not ok4, "passed>total 应拦"
    ok5, _ = check_port_readiness({"tests": {"migrated": True, "total": 1, "passed": 1}})
    assert not ok5, "缺 target 应拦"

    print("PASS: L92 移植等价性，5 条断言全过（L2 两条全覆盖+3 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
