# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L74 并发写冲突闸 — 两人同时改同一份文件，后写的会盖掉先写的。

L1: 检测多 agent 对同一资源的写意图重叠（资源路径+时间窗），重叠 → 冲突报告。
L2: ①同资源双写意图报冲突 ②不同资源放行。
"""


def _overlap(win_a, win_b):
    """开区间时间窗重叠判定: [s1,e1] 与 [s2,e2]。端点相接不算重叠。"""
    return win_a[0] < win_b[1] and win_b[0] < win_a[1]


def write_gate(intents):
    """intents: [{agent, resource, window: (start, end)}]

    返回 {"conflicts": [{resource, agents, windows}], "clear": [放行的资源]}
    """
    if not isinstance(intents, list):
        raise ValueError("intents 必须是列表")
    conflicts, by_res = [], {}
    for it in intents:
        by_res.setdefault(it["resource"], []).append(it)
    for res, group in by_res.items():
        hit = []
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if _overlap(group[i]["window"], group[j]["window"]):
                    hit.append((group[i]["agent"], group[j]["agent"],
                                group[i]["window"], group[j]["window"]))
        if hit:
            conflicts.append({"resource": res, "agents": sorted({a for h in hit for a in h[:2]}),
                              "pairs": hit})
    clear = [r for r, g in by_res.items()
             if not any(c["resource"] == r for c in conflicts)]
    return {"conflicts": conflicts, "clear": clear}


def main():
    a = [{"agent": "A", "resource": "src/api.py", "window": (10, 20)},
         {"agent": "B", "resource": "src/api.py", "window": (15, 30)}]
    b = [{"agent": "A", "resource": "src/api.py", "window": (10, 20)},
         {"agent": "B", "resource": "src/ui.py", "window": (15, 30)}]
    ra, rb = write_gate(a), write_gate(b)
    print("场景A: 冲突=%s → 后写会盖掉先写，需决定谁先" %
          [(c["resource"], c["agents"]) for c in ra["conflicts"]])
    print("场景B: 冲突=%s 放行=%s → 各写各的，不拦" % (rb["conflicts"], rb["clear"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
