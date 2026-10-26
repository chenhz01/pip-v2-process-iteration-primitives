# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L86 信用衰减回摊：检索按（来源信用 × 时间衰减）排序加权，低分降权不删除。"""

import math

DEFAULT_HALFLIFE_DAYS = 30.0  # 半衰期：默认 30 天后信用减半


def credit_score(entry, halflife_days=DEFAULT_HALFLIFE_DAYS):
    """score = credit * 0.5^(age_days / halflife)。entry: {"credit", "age_days"}。"""
    return entry["credit"] * math.pow(0.5, entry["age_days"] / halflife_days)


def rank_memories(memories, halflife_days=DEFAULT_HALFLIFE_DAYS):
    """按衰减后信用分从高到低排序；返回 [(entry, score)]。不删除任何条目。"""
    scored = [(m, credit_score(m, halflife_days)) for m in memories]
    scored.sort(key=lambda p: p[1], reverse=True)
    return scored


if __name__ == "__main__":
    mems = [
        {"id": "m1", "credit": 0.9, "age_days": 1},
        {"id": "m2", "credit": 0.3, "age_days": 360},
        {"id": "m3", "credit": 0.6, "age_days": 30},
    ]
    ranked = rank_memories(mems)
    for entry, score in ranked:
        print(f"[demo] {entry['id']}: 信用={entry['credit']} 年龄={entry['age_days']}天 -> 衰减分={score:.4f}")
    print(f"判了什么: 高信新记忆 m1 排第 1，旧低信记忆 m2 排最后（降权未删除，仍保留 {len(mems)} 条）")
