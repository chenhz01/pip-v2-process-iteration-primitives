# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L94 撤销唯一性实测：破坏性操作前校验——撤销路径存在且唯一，
且撤销路径本身被实际演练过（有演练记录）。
（与 v1 L39 区别：v1 查快照存在性，本件查唯一性+真按过一次）
"""


def gate_destructive_op(op):
    """放行前闸门。op 字段：
      op_name     —— 操作名（必填）
      undo_paths  —— 撤销路径列表（应恰好 1 条）
      rehearsal   —— {"path": 演练的是哪条, "ok": 是否真成功, "at": 何时}
    返回 (ok, reason)。
    """
    if not isinstance(op, dict) or not (op.get("op_name") or "").strip():
        return False, "缺 op_name，不知道要按哪个危险按钮"
    paths = op.get("undo_paths") or []
    if len(paths) == 0:
        return False, "无撤销路径：破坏性操作不许裸奔"
    if len(paths) > 1:
        return False, "撤销路径有 %d 条不唯一：真出事时按错一条就是二次事故" % len(paths)
    rehe = op.get("rehearsal") or {}
    if not isinstance(rehe, dict) or not rehe.get("ok"):
        return False, "撤销路径「%s」从未实测演练：按钮必须真按过一次、真管用" % paths[0]
    if rehe.get("path") != paths[0]:
        return False, "演练的是「%s」不是待用路径「%s」：演练对不上号等于没演" % (
            rehe.get("path"), paths[0])
    return True, "撤销路径唯一（%s）且已实测演练通过，放行" % paths[0]


if __name__ == "__main__":
    cases = [
        ("无撤销路径", {"op_name": "drop-table", "undo_paths": []}),
        ("双路径不唯一", {"op_name": "drop-table",
                          "undo_paths": ["restore-snapshot", "replay-binlog"]}),
        ("唯一但没练过", {"op_name": "drop-table",
                          "undo_paths": ["restore-snapshot"]}),
        ("练的是另一条", {"op_name": "drop-table", "undo_paths": ["restore-snapshot"],
                          "rehearsal": {"path": "replay-binlog", "ok": True, "at": "2026-10-20"}}),
        ("唯一且演练过", {"op_name": "drop-table", "undo_paths": ["restore-snapshot"],
                          "rehearsal": {"path": "restore-snapshot", "ok": True,
                                        "at": "2026-10-25"}}),
    ]
    for name, c in cases:
        ok, why = gate_destructive_op(c)
        print("判例[%s] 放行=%s —— %s" % (name, ok, why))
