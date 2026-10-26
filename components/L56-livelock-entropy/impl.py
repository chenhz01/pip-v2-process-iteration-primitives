# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L56 活锁熵检：agent 是否"忙但没进展"。

只看动作签名（字符串），不做语义理解：对连续 N 步动作序列算
窗口集合熵，重复度高（熵低）且窗口期无新事实产出 -> 判活锁。
"""

import math


def window_entropy(actions, window=6):
    """窗口内动作签名的集合熵：0=完全单一，log2(k)=k 种均匀分布。"""
    seg = list(actions)[-window:]
    counts = {}
    for a in seg:
        counts[a] = counts.get(a, 0) + 1
    n = len(seg)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def detect_livelock(actions, new_facts=(), window=6, entropy_threshold=1.0):
    """判活锁：窗口熵 <= 阈值（重复度高）且窗口期无新事实。

    返回 (is_livelock, info)；info 含熵值、新事实数与判决理由。
    """
    if len(actions) < 2:
        return False, {"verdict": "SKIP", "why": "动作序列过短（<2），不判"}
    ent = window_entropy(actions, window)
    no_new_fact = len(set(new_facts)) == 0
    hit = ent <= entropy_threshold and no_new_fact
    if hit:
        why = "窗口熵 %.3f<=阈 %.1f 且无新事实，原地打转" % (ent, entropy_threshold)
    elif not no_new_fact:
        why = "有 %d 项新事实产出，重复也算进展" % len(set(new_facts))
    else:
        why = "窗口熵 %.3f>阈 %.1f，动作足够多样" % (ent, entropy_threshold)
    return hit, {"verdict": "LIVELOCK" if hit else "NORMAL",
                 "window_entropy": round(ent, 3),
                 "threshold": entropy_threshold,
                 "new_facts": len(set(new_facts)), "why": why}


if __name__ == "__main__":
    _, i1 = detect_livelock(["A", "B", "A", "B", "A", "B"], new_facts=[])
    print("案例1 [A,B,A,B,A,B] 无新产物 ->", i1["verdict"],
          "窗口熵=", i1["window_entropy"], "理由:", i1["why"])
    _, i2 = detect_livelock(["A", "B", "C"], new_facts=["artifact_1"])
    print("案例2 [A,B,C] 带新产物   ->", i2["verdict"],
          "窗口熵=", i2["window_entropy"], "理由:", i2["why"])
    _, i3 = detect_livelock(["A", "B", "A", "B"], new_facts=["f1", "f2"])
    print("案例3 重复动作但有新事实 ->", i3["verdict"], "理由:", i3["why"])
