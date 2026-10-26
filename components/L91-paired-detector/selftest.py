# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L91 selftest：断言对齐卡片 L2（①无检测件判未完成 ②有检测件放行）。"""

import sys

from impl import check_fix_completeness


def main():
    # L2-1 无检测件 → 判未完成
    ok1, why1 = check_fix_completeness({"fixed_target": "空指针越界"})
    assert not ok1, "L2-1 失败：无检测件应判未完成"
    assert "检测件" in why1, "拒绝理由应点名检测件缺失"

    # L2-2 有检测件 → 放行
    ok2, why2 = check_fix_completeness({
        "fixed_target": "空指针越界",
        "detection": {"kind": "monitor", "location": "metrics/panic_counter"}})
    assert ok2, "L2-2 失败：有检测件应放行"
    assert "monitor" in why2

    # 负对照：坏输入（缺 fixed_target / 假 kind）也要拦
    ok3, why3 = check_fix_completeness({})
    assert not ok3 and "fixed_target" in why3, "空产物应被拦"
    ok4, _ = check_fix_completeness({
        "fixed_target": "x", "detection": {"kind": " README", "location": "here"}})
    assert not ok4, "非法 kind 应被拦"

    print("PASS: L91 检测件伴随，4 条断言全过（L2 两条全覆盖+2 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
