# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L63 评测成本比：盯一个比值——检查花费 ÷ 干活花费。

检查比干活还贵数倍，就该换检查方式。L1：输入两侧花费，算比值，
超阈报警并给三条降本路径。
"""

REDUCTION_PATHS = (
    "抽样评测：全量改分层抽样，只深审可疑子集",
    "廉价预筛前置：L1 规则先扫，贵的 L2 只看放行集",
    "评测缓存：相同输入指纹直接复用历史评测结果",
)


def eval_cost_ratio(eval_cost, work_cost, alarm_threshold=3.0):
    """返回 {"ratio", "alarm", "threshold", "paths"}。

    ratio = eval_cost / work_cost；work_cost 必须为正。
    """
    if work_cost <= 0:
        raise ValueError("work_cost 必须为正，否则比值无意义")
    ratio = eval_cost / work_cost
    alarm = ratio > alarm_threshold
    return {"ratio": round(ratio, 3),
            "alarm": alarm,
            "threshold": alarm_threshold,
            "paths": list(REDUCTION_PATHS) if alarm else []}


if __name__ == "__main__":
    r1 = eval_cost_ratio(500.0, 100.0)
    print("案例1 评测500/干活100 -> 比值 %.1f，%s（阈 %.1f）"
          % (r1["ratio"], "报警" if r1["alarm"] else "正常", r1["threshold"]))
    if r1["alarm"]:
        for i, p in enumerate(r1["paths"], 1):
            print("  降本路径%d: %s" % (i, p))
    r2 = eval_cost_ratio(50.0, 100.0)
    print("案例2 评测50/干活100  -> 比值 %.1f，%s"
          % (r2["ratio"], "报警" if r2["alarm"] else "正常"))
    r3 = eval_cost_ratio(300.0, 100.0)
    print("案例3 评测300/干活100 -> 比值 %.1f，%s（恰在阈上不报）"
          % (r3["ratio"], "报警" if r3["alarm"] else "正常"))
