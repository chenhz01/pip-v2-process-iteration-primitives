# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L60 每步档位策略：不是每步都值得动用最大火力。

L1：输入步骤特征（可逆性/影响面/历史失败率），输出档位
（cheap/balanced/max），纯规则、可解释、可追溯。
"""


def pick_gear(reversible, blast_radius, failure_rate=0.0):
    """按步骤特征输出 (gear, why)。

    规则（按序命中即返回）：
      1. 不可逆 且 影响面>=3            -> max
      2. 可逆 且 影响面<=1 且 失败率<0.3 -> cheap
      3. 其余                           -> balanced
    """
    if not reversible and blast_radius >= 3:
        return "max", "不可逆+影响面 %d，必须最大火力" % blast_radius
    if reversible and blast_radius <= 1 and failure_rate < 0.3:
        return "cheap", "可逆+低影响 %d+低失败率 %.2f，便宜档足够" \
            % (blast_radius, failure_rate)
    return "balanced", "特征混合（可逆=%s，影响面=%d，失败率=%.2f）" \
        % (reversible, blast_radius, failure_rate)


def decide(step):
    """step: {"reversible": bool, "blast_radius": int, "failure_rate": float}"""
    gear, why = pick_gear(step.get("reversible", True),
                          step.get("blast_radius", 1),
                          step.get("failure_rate", 0.0))
    return {"gear": gear, "why": why}


if __name__ == "__main__":
    for name, step in [
        ("改本地草稿", {"reversible": True, "blast_radius": 1, "failure_rate": 0.1}),
        ("生产库 schema 迁移", {"reversible": False, "blast_radius": 5, "failure_rate": 0.2}),
        ("批量通知用户", {"reversible": True, "blast_radius": 4, "failure_rate": 0.4}),
    ]:
        r = decide(step)
        print("步骤[%s] -> 档位=%s 理由: %s" % (name, r["gear"], r["why"]))
