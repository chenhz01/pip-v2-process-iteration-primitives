# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L68 冷启动恢复测试 — 空白上下文只读 checkpoint，新伙伴能否复述四项。

L1: 只凭存档本身尝试复述 目标/已完成/下一步/约束，四项任一复述不出 → 判存档不合格。
L2: ①四项齐判 PASS ②缺「下一步」判 FAIL。
"""

FIELDS = ("goal", "completed", "next_step", "constraints")
FIELD_ZH = {"goal": "目标", "completed": "已完成", "next_step": "下一步", "constraints": "约束"}


def cold_start_check(checkpoint):
    """用空白上下文只读 checkpoint，模拟新伙伴复述四项。

    返回 {"pass": bool, "missing": [...], "recite": {字段: 值}}
    """
    if not isinstance(checkpoint, dict):
        return {"pass": False, "missing": list(FIELDS), "recite": {}}
    missing = [f for f in FIELDS if not str(checkpoint.get(f, "")).strip()]
    recite = {f: checkpoint.get(f, "") for f in FIELDS}
    return {"pass": not missing, "missing": missing, "recite": recite}


def main():
    good = {"goal": "交付报表模块", "completed": "解析器已写完并通过单测",
            "next_step": "实现渲染层，接口契约见 api.md", "constraints": "不得引入新依赖"}
    bad = {"goal": "交付报表模块", "completed": "解析器已写完", "constraints": "不得引入新依赖"}
    g = cold_start_check(good)
    b = cold_start_check(bad)
    print("存档A: 四项复述=%s → %s" % (g["pass"], "合格，新伙伴可直接接手" if g["pass"] else "不合格"))
    print("  复述样例: 目标=%s | 下一步=%s" % (g["recite"]["goal"], g["recite"]["next_step"]))
    print("存档B: pass=%s 缺失=%s → 坏存档，接手人会不知道干什么" % (b["pass"], b["missing"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
