# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L69 状态完整性断言 — 恢复现场后对照执行前快照逐项点数。

L1: 恢复后对照快照断言（键集合+值类型），输出缺失清单。
L2: ①缺键报缺 ②全齐报 PASS。
"""

REQUIRED = ("dialog", "variables", "intermediates")


def integrity_check(snapshot, restored):
    """对照执行前快照逐项断言键存在与类型一致。

    返回 {"pass": bool, "missing": [...], "type_mismatch": {键: (期望, 实际)}}
    """
    if not isinstance(snapshot, dict) or not isinstance(restored, dict):
        return {"pass": False, "missing": list(REQUIRED), "type_mismatch": {}}
    missing = sorted(k for k in snapshot if k not in restored)
    mismatch = {}
    for k, v in snapshot.items():
        if k in restored and type(restored[k]) is not type(v):
            mismatch[k] = (type(v).__name__, type(restored[k]).__name__)
    return {"pass": not missing and not mismatch,
            "missing": missing, "type_mismatch": mismatch}


def main():
    snapshot = {"dialog": ["u1", "a1"], "variables": {"n": 3}, "intermediates": [1, 2], "extra": "x"}
    ok = integrity_check(snapshot, dict(snapshot))
    bad = integrity_check(snapshot, {"dialog": ["u1"], "variables": "坏了", "extra": "x"})
    print("现场A: 全齐且类型一致 → pass=%s" % ok["pass"])
    print("现场B: 缺失=%s 类型不符=%s → 先补齐再跑，别急着执行" % (bad["missing"], bad["type_mismatch"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
