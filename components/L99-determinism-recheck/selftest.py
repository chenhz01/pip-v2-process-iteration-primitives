# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L99 selftest：断言对齐卡片 L2（①两次不一致摘标记 ②一致保留）。"""

import sys

from impl import recheck_determinism, stable_step


def varying():
    varying.n = getattr(varying, "n", 0) + 1
    return "out-" + str(varying.n)


def main():
    # L2-1 两次不一致 → 撤销确定性标记
    keep1, d1 = recheck_determinism("藏状态步骤", varying)
    assert not keep1, "L2-1 失败：两次不一致应摘标记"
    assert d1["verdict"] == "REVOKE" and "不一致" in d1["reason"]

    # L2-2 一致 → 保留标记
    keep2, d2 = recheck_determinism("纯函数步骤", stable_step)
    assert keep2, "L2-2 失败：两次一致应保留标记"
    assert d2["verdict"] == "KEEP"
    assert d2["out_a"] == d2["out_b"]

    # 负对照：空串两次一致应保留；数值两次一致同样保留（类型不掺水）
    keep3, _ = recheck_determinism("空输出", lambda: "")
    assert keep3, "两次空串一致应保留标记"
    keep4, d4 = recheck_determinism("数值输出", lambda: 5)
    assert keep4 and d4["verdict"] == "KEEP" and d4["out_a"] == 5

    print("PASS: L99 确定性复验，5 条断言全过（L2 两条全覆盖+2 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
