# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L57 死锁等待图：谁在等谁，成环即死锁。

从各 agent 状态采集 waiting_on 关系，建有向图，DFS 找环。
只有"正在等待"的节点才参与建边：等一个已在跑的伙伴不算环。
"""


def find_deadlock(waiting_on):
    """waiting_on: {agent: 被等待者或 None}。返回 (has_cycle, cycle)。"""
    graph = {a: w for a, w in waiting_on.items() if w}
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    cycle = []

    def dfs(node, stack):
        color[node] = GRAY
        stack.append(node)
        nxt = graph.get(node)
        if nxt in graph:
            if color[nxt] == GRAY:
                cycle.extend(stack[stack.index(nxt):])
                return True
            if color[nxt] == WHITE and dfs(nxt, stack):
                return True
        color[node] = BLACK
        stack.pop()
        return False

    for n in list(graph):
        if color[n] == WHITE and dfs(n, []):
            return True, cycle
    return False, []


def check_agents(states):
    """states: {agent: {"waiting_on": 名字或 None}}。死锁则返回环成员。"""
    waiting = {a: s.get("waiting_on") for a, s in states.items()}
    has_cycle, cycle = find_deadlock(waiting)
    return has_cycle, {"verdict": "DEADLOCK" if has_cycle else "OK",
                       "cycle": cycle}


if __name__ == "__main__":
    bad, i1 = check_agents({"A": {"waiting_on": "B"},
                            "B": {"waiting_on": "A"}})
    ring = "->".join(i1["cycle"] + [i1["cycle"][0]])
    print("案例1 A等B、B等A ->", i1["verdict"], "环:", ring)
    good, i2 = check_agents({"A": {"waiting_on": "B"},
                             "B": {"waiting_on": None}})
    print("案例2 A等B、B在跑 ->", i2["verdict"])
    _, i3 = check_agents({"A": {"waiting_on": "B"},
                          "B": {"waiting_on": "C"},
                          "C": {"waiting_on": None}})
    print("案例3 A等B、B等C、C在跑 ->", i3["verdict"])
