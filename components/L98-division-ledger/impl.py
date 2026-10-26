# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L98 分工账本：每一步记清楚是代码干的还是模型干的、花了多少；
月底一看就知道钱去哪了。缺类型标记的步骤必须列出来——不知道谁花的账不能留。
"""

VALID_EXECUTORS = ("code", "model")


def build_ledger(steps):
    """steps: [{"step": 名, "executor": "code"|"model"|None, "cost": 数值}]
    返回 {"by_type": {code/model 成本合计}, "ratio": code/model 比,
          "untagged": 缺类型标记的步骤名清单, "total": 总成本}
    """
    if not steps:
        return {"by_type": {"code": 0.0, "model": 0.0}, "ratio": None,
                "untagged": [], "total": 0.0, "reason": "账本为空"}
    by_type = {"code": 0.0, "model": 0.0}
    untagged = []
    for s in steps:
        if not isinstance(s, dict) or not s.get("step"):
            untagged.append("<无名步骤>")
            continue
        ex, cost = s.get("executor"), s.get("cost", 0.0)
        if not isinstance(cost, (int, float)) or cost < 0:
            untagged.append(s["step"] + "(成本非法)")
            continue
        if ex in VALID_EXECUTORS:
            by_type[ex] += float(cost)
        else:
            untagged.append(s["step"])
    total = by_type["code"] + by_type["model"]
    ratio = None
    if by_type["model"] > 0:
        ratio = round(by_type["code"] / by_type["model"], 3)
    reason = "账本可按类型汇总：code=%.1f, model=%.1f, 合计=%.1f" % (
        by_type["code"], by_type["model"], total)
    if untagged:
        reason += "；%d 步缺类型标记：%s" % (len(untagged), ", ".join(untagged))
    return {"by_type": by_type, "ratio": ratio, "untagged": untagged,
            "total": total, "reason": reason}


if __name__ == "__main__":
    ledger = build_ledger([
        {"step": "解析日志", "executor": "code", "cost": 0.2},
        {"step": "判断根因", "executor": "model", "cost": 3.0},
        {"step": "生成补丁", "executor": "model", "cost": 2.0},
        {"step": "跑测试", "executor": "code", "cost": 0.5},
        {"step": "临场发挥", "executor": None, "cost": 1.0},
    ])
    print("分工账本：code=%.1f / model=%.1f（比=%.1f）总=%.1f" % (
        ledger["by_type"]["code"], ledger["by_type"]["model"],
        ledger["ratio"], ledger["total"]))
    print("判语：%s" % ledger["reason"])
