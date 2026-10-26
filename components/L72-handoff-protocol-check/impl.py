# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L72 交接协议完整性 — 交接单必须写全，缺项的交接单不许收。

L1: 校验交接包必填字段（状态/阻塞/下一步/权限边界），缺项拒收并列缺失。
L2: ①缺「阻塞项」拒收 ②齐全签收。
"""

REQUIRED = ("status", "blockers", "next_step", "permission_boundary")
FIELD_ZH = {"status": "状态", "blockers": "阻塞项", "next_step": "下一步",
            "permission_boundary": "权限边界"}


def handoff_check(handoff):
    """校验交接包必填字段，缺项拒收。

    返回 {"accept": bool, "missing": [...], "note": ...}
    """
    if not isinstance(handoff, dict):
        return {"accept": False, "missing": list(REQUIRED), "note": "交接包必须是结构化对象"}
    missing = [f for f in REQUIRED
               if not isinstance(handoff.get(f), (str, list)) or
               (isinstance(handoff.get(f), str) and not handoff.get(f).strip())]
    # 空列表（如 blockers: []）是「明确无阻塞」的合法写法，算写全；
    # 只有空白字符串/缺失/类型不对才算缺项。
    note = "签收，开始接手" if not missing else "拒收，缺: " + "、".join(FIELD_ZH[f] for f in missing)
    return {"accept": not missing, "missing": missing, "note": note}


def main():
    good = {"status": "解析器完成，测试 12/12 过", "blockers": [],
            "next_step": "B 负责 API 层，契约见 api.md", "permission_boundary": "只许写 api/ 目录"}
    bad = {"status": "解析器完成", "next_step": "B 负责 API 层",
           "permission_boundary": "只许写 api/ 目录"}
    g = handoff_check(good)
    b = handoff_check(bad)
    print("交接单A: accept=%s → %s" % (g["accept"], g["note"]))
    print("交接单B: accept=%s 缺=%s → %s" % (b["accept"], b["missing"], b["note"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
