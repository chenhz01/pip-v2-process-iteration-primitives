# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L59 循环预算熔断：给"原地打转"设硬性花费上限。

L1：记录无新信息步数与累计花费，任一超阈 -> 返回 HALT 信号，
不许再烧。有新信息的正常产出不受此件拦截。
"""


def loop_budget_halt(no_new_info_steps, cumulative_cost,
                     cost_limit=10.0, no_info_limit=5):
    """无新信息步数 或 累计花费 任一超阈 -> HALT。

    返回 (should_halt, info)；info 含两条预算线各自是否越线及理由。
    """
    over_stall = no_new_info_steps >= no_info_limit
    over_cost = cumulative_cost >= cost_limit
    halt = over_stall or over_cost
    info = {
        "signal": "HALT" if halt else "CONTINUE",
        "no_new_info_steps": no_new_info_steps,
        "no_info_limit": no_info_limit,
        "cumulative_cost": cumulative_cost,
        "cost_limit": cost_limit,
        "over_stall": over_stall,
        "over_cost": over_cost,
    }
    if halt:
        why = []
        if over_stall:
            why.append("连续 %d 步无新信息（限 %d）"
                       % (no_new_info_steps, no_info_limit))
        if over_cost:
            why.append("累计花费 %.2f 达/超阈 %.2f"
                       % (cumulative_cost, cost_limit))
        info["why"] = "；".join(why) + "，强制停"
    else:
        info["why"] = "每步都有新信息且花费未超阈，继续"
    return halt, info


if __name__ == "__main__":
    h1, i1 = loop_budget_halt(5, 12.0)
    print("案例1 5步无新信息+花费12 ->", i1["signal"], "理由:", i1["why"])
    h2, i2 = loop_budget_halt(0, 4.0)
    print("案例2 有新信息+花费4    ->", i2["signal"], "理由:", i2["why"])
    h3, i3 = loop_budget_halt(2, 11.0)
    print("案例3 花费超阈但步数未超 ->", i3["signal"], "理由:", i3["why"])
