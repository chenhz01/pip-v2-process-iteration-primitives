# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L98 selftest：断言对齐卡片 L2（①账本能按类型汇总 ②缺类型标记的步骤被列出）。"""

import sys

from impl import build_ledger


def main():
    steps = [
        {"step": "解析", "executor": "code", "cost": 1.0},
        {"step": "推断", "executor": "model", "cost": 4.0},
        {"step": "黑箱步骤", "executor": None, "cost": 2.0},
        {"step": "另一黑箱"},
    ]
    led = build_ledger(steps)
    # L2-1 账本能按类型汇总
    assert led["by_type"]["code"] == 1.0, "L2-1 失败：code 合计应为 1.0"
    assert led["by_type"]["model"] == 4.0, "L2-1 失败：model 合计应为 4.0"
    assert led["ratio"] == 0.25, "code/model 比应为 0.25"
    # L2-2 缺类型标记的步骤被列出
    assert led["untagged"] == ["黑箱步骤", "另一黑箱"], "L2-2 失败：未标记步骤应全部列出"
    assert "缺类型标记" in led["reason"]

    # 负对照：空账本、成本非法都进 untagged
    empty = build_ledger([])
    assert empty["total"] == 0.0 and empty["by_type"] == {"code": 0.0, "model": 0.0}
    bad = build_ledger([{"step": "x", "executor": "code", "cost": -5}])
    assert bad["untagged"] == ["x(成本非法)"], "负成本应进非法清单"

    print("PASS: L98 分工账本，6 条断言全过（L2 两条全覆盖+2 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
