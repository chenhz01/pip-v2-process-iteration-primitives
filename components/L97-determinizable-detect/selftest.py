# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L97 selftest：断言对齐卡片 L2（①100 次恒定建议固化 ②输出有变化不建议）。"""

import sys

from impl import determinizable_verdict


def mk(n, out="OK", failed=False):
    return [{"input_sig": "fixed-A", "output": out, "failed": failed} for _ in range(n)]


def main():
    # L2-1 100 次恒定 → 建议固化
    v1 = determinizable_verdict(mk(100))
    assert v1["suggest"], "L2-1 失败：100 次恒定+零失败应建议固化"
    assert "恒定" in v1["reason"]

    # L2-2 输出有变化 → 不建议
    v2 = determinizable_verdict(mk(99) + [{"input_sig": "fixed-A", "output": "B", "failed": False}])
    assert not v2["suggest"], "L2-2 失败：输出有变化不建议固化"
    assert "输出" in v2["reason"]

    # 负对照：有失败 / 样本不足都不建议
    v3 = determinizable_verdict(mk(9, failed=True) + mk(1))
    assert not v3["suggest"], "有失败不建议固化"
    v4 = determinizable_verdict(mk(2))
    assert not v4["suggest"], "样本不足不建议固化"

    print("PASS: L97 可确定化检测，4 条断言全过（L2 两条全覆盖+2 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
