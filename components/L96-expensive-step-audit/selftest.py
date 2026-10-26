# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L96 selftest：断言对齐卡片 L2（①缺替代方案字段拦截 ②齐全放行）。"""

import sys

from impl import audit_expensive_step, scan_plan


def main():
    # L2-1 缺替代方案字段 → 拦截
    ok1, why1 = audit_expensive_step({
        "name": "全量重建", "expensive": True,
        "audit": {"necessity": "索引损坏"}})
    assert not ok1, "L2-1 失败：缺 alternative 应拦截"
    assert "alternative" in why1

    # L2-2 齐全 → 放行
    ok2, why2 = audit_expensive_step({
        "name": "全量回归", "expensive": True,
        "audit": {"necessity": "发布前唯一可信验证",
                  "alternative": "抽样 200 例先跑"}})
    assert ok2, "L2-2 失败：审计齐全应放行"

    # 负对照：无审计记录 / 缺必要性 / 连 name 都没有都要拦；非昂贵直接过
    ok3, _ = audit_expensive_step({"name": "重建", "expensive": True})
    assert not ok3, "昂贵且零审计应拦"
    ok4, _ = audit_expensive_step({
        "name": "重建", "expensive": True,
        "audit": {"alternative": "没有替代，必须做"}})
    assert not ok4, "缺 necessity 应拦"
    ok5, _ = audit_expensive_step({"expensive": True, "audit": {"necessity": "n", "alternative": "a"}})
    assert not ok5, "缺 name 应拦"
    ok6, why6 = audit_expensive_step({"name": "grep", "expensive": False})
    assert ok6, "非昂贵步骤无需过堂应放行"

    ok_n, blocked = scan_plan([{"name": "a", "expensive": True}])
    assert ok_n == 0 and len(blocked) == 1
    print("PASS: L96 昂贵步骤前置审计，7 条断言全过（L2 两条全覆盖+4 负对照+批量扫描）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
