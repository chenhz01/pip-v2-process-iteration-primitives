# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L100 selftest：断言对齐卡片 L2（①无源数字被拦 ②有源数字放行）。"""

import sys

from impl import gate_numbers


def main():
    # L2-1 无源数字被拦
    r1 = gate_numbers([{"text": "性能提升 45 个百分点"}])
    assert r1["blocked"] == [("45", "性能提升 45 个百分点")], "L2-1 失败：无源数字应被拦"
    assert not r1["passed"]

    # L2-2 有源数字放行
    r2 = gate_numbers([{"text": "实测 55/55 可跑", "source": "selftest.py 退出码 0"}])
    assert r2["blocked"] == [], "L2-2 失败：有源数字应放行"
    assert r2["passed"] == 1

    # 负对照：空来源串 / 多个无源数字 / 坏输入都要拦
    r3 = gate_numbers([{"text": "耗时 3.2 秒", "source": "   "}])
    assert r3["blocked"] == [("3.2", "耗时 3.2 秒")], "空串来源等于没来源"
    r4 = gate_numbers([{"text": "从 10 涨到 25 再到 100"}])
    assert [n for n, _ in r4["blocked"]] == ["10", "25", "100"], "每个无源数字单独拦"
    r5 = gate_numbers("not-a-list")
    assert r5["blocked"] == [] and "无法审" in r5["reason"], "坏输入不崩、显式拒审"

    print("PASS: L100 无源数字拦截，5 条断言全过（L2 两条全覆盖+3 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
