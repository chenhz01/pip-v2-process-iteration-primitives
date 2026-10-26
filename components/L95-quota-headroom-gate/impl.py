# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L95 配额余量闸：开新任务前看一眼钱包和油表——本月额度还剩多少？
这单要烧多少？不够就拒开或降档，不许开了再发现烧穿。
（来源：harp 配额余量）
"""

DENY = "DENY"
DOWNGRADE = "DOWNGRADE"
ALLOW = "ALLOW"


def quota_gate(used, cap, task_cost, safety_margin=0.0):
    """按配额日志（窗口用量 used + 上限 cap）预算新任务消耗 task_cost。
    safety_margin 为必须留出的余量。返回 (verdict, detail)。
    """
    for name, v in (("used", used), ("cap", cap), ("task_cost", task_cost)):
        if not isinstance(v, (int, float)) or v < 0 or v != v:
            return DENY, {"reason": "配额日志字段 %s 非法（%r），数据先洗干净再谈预算" % (name, v)}
    if cap <= 0:
        return DENY, {"reason": "上限 cap=%r 无效：没有额度就别开工" % cap}
    if used > cap:
        return DENY, {"reason": "配额已烧穿：used=%.1f > cap=%.1f" % (used, cap)}
    remaining = cap - used
    need = task_cost + safety_margin
    if task_cost > remaining:
        return DENY, {"reason": "余量不足：剩余 %.1f < 本单预计 %.1f，拒开" % (remaining, task_cost),
                      "remaining": remaining}
    if need > remaining:
        return DOWNGRADE, {"reason": "余量 %.1f 只够原样任务，留 %.1f 安全垫就得降档" % (
                               remaining, safety_margin),
                           "remaining": remaining}
    return ALLOW, {"reason": "余量 %.1f，本单 %.1f + 安全垫 %.1f 装得下，放行" % (
                       remaining, task_cost, safety_margin),
                   "remaining": remaining}


if __name__ == "__main__":
    cases = [
        ("余额充足", (120.0, 500.0, 80.0, 0.0)),
        ("余量吃紧", (120.0, 500.0, 380.0, 20.0)),
        ("余量不足", (450.0, 500.0, 80.0, 0.0)),
        ("日志烧穿", (520.0, 500.0, 10.0, 0.0)),
        ("日志非法", (float("nan"), 500.0, 10.0, 0.0)),
    ]
    for name, (u, c, t, m) in cases:
        v, d = quota_gate(u, c, t, m)
        print("判例[%s] %s —— %s" % (name, v, d["reason"]))
