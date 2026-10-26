# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L94 selftest：断言对齐卡片 L2（①撤销未演练拦截 ②已演练放行）。"""

import sys

from impl import gate_destructive_op


def main():
    # L2-1 撤销未演练 → 拦截
    ok1, why1 = gate_destructive_op({"op_name": "rm-caches", "undo_paths": ["backup-dir"]})
    assert not ok1, "L2-1 失败：未演练的撤销路径应拦截"
    assert "演练" in why1

    # L2-2 已演练 → 放行
    ok2, why2 = gate_destructive_op({
        "op_name": "rm-caches", "undo_paths": ["backup-dir"],
        "rehearsal": {"path": "backup-dir", "ok": True, "at": "2026-10-25"}})
    assert ok2, "L2-2 失败：唯一且已演练应放行"
    assert "唯一" in why2

    # 负对照：无路径 / 不唯一 / 演练对不上号都要拦
    ok3, _ = gate_destructive_op({"op_name": "x", "undo_paths": []})
    assert not ok3, "无撤销路径应拦"
    ok4, _ = gate_destructive_op({"op_name": "x", "undo_paths": ["a", "b"]})
    assert not ok4, "路径不唯一应拦"
    ok5, _ = gate_destructive_op({
        "op_name": "x", "undo_paths": ["a"],
        "rehearsal": {"path": "b", "ok": True}})
    assert not ok5, "演练路径与待用路径不一致应拦"

    print("PASS: L94 撤销唯一性实测，5 条断言全过（L2 两条全覆盖+3 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
