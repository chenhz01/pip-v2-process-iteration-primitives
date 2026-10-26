# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L61 廉价预筛：便宜办法全量扫一遍，可疑子集才交贵的深审。

L1：规则/关键词分类器（L1 层）全量扫，只放行可疑子集给 L2；
输出召回率下界估计。规则表为空时显式报「无法分诊」，绝不放行全部。
"""

DEFAULT_RULES = ("error", "timeout", "leak", "abnormal")


def cheap_prefilter(records, rules=None):
    """records: 字符串列表；rules: 关键词元组/列表。

    返回 (suspects, info)。规则表为空 -> raise ValueError（显式拒绝）。
    recall_lb：可疑占比，作为召回率下界的保守估计口径。
    """
    if rules is None:
        rules = DEFAULT_RULES
    rules = list(rules)
    if not rules:
        raise ValueError("无法分诊：规则表为空，拒绝放行全部记录")
    suspects = [r for r in records if any(kw in r for kw in rules)]
    info = {
        "total": len(records),
        "flagged": len(suspects),
        "passed_to_expensive": len(suspects),
        "recall_lower_bound_estimate":
            round(len(suspects) / len(records), 3) if records else 1.0,
        "rules_used": len(rules),
    }
    return suspects, info


if __name__ == "__main__":
    logs = ["ok: job done", "error: db timeout", "ok: cached",
            "error: memory leak", "ok: heartbeat"]
    sus, info = cheap_prefilter(logs)
    print("案例1 5 条日志、规则 %d 条 -> 放行 %d 条深审，召回下界估计 %.3f"
          % (info["rules_used"], info["flagged"],
             info["recall_lower_bound_estimate"]))
    print("  可疑集:", sus)
    try:
        cheap_prefilter(logs, rules=[])
    except ValueError as e:
        print("案例2 空规则表 -> 显式报错:", e)
