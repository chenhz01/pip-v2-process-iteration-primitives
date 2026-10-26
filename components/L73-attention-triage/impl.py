# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L73 注意力分诊 — 多伙伴并行时回答：谁在等我？谁的事最急？

L1: 汇总各协作者状态（working/waiting/done），按阻塞链长度+等待时长排优先级。
L2: ①被阻塞链最长的排最前 ②done 的不占队列。
"""


def triage(collaborators):
    """collaborators: [{name, status, waiting_seconds, blocked_chain}]

    只让 waiting 的进队列；优先级 = 阻塞链长度优先、等待时长次之（字典序降序）。
    返回 {"queue": [按急迫度排序的名单], "excluded_done": [...], "excluded_working": [...]}
    """
    if not isinstance(collaborators, list):
        raise ValueError("collaborators 必须是列表")
    queue = sorted(
        (c for c in collaborators if c.get("status") == "waiting"),
        key=lambda c: (c.get("blocked_chain", 0), c.get("waiting_seconds", 0)),
        reverse=True)
    return {
        "queue": [c["name"] for c in queue],
        "excluded_done": [c["name"] for c in collaborators if c.get("status") == "done"],
        "excluded_working": [c["name"] for c in collaborators if c.get("status") == "working"],
    }


def main():
    team = [
        {"name": "A", "status": "waiting", "waiting_seconds": 30, "blocked_chain": 3},
        {"name": "B", "status": "waiting", "waiting_seconds": 600, "blocked_chain": 1},
        {"name": "C", "status": "working", "waiting_seconds": 0, "blocked_chain": 0},
        {"name": "D", "status": "done", "waiting_seconds": 0, "blocked_chain": 0},
    ]
    r = triage(team)
    print("队列优先级: %s（A 链最长排最前，B 虽等得久但链短居次）" % r["queue"])
    print("不占队列: done=%s working=%s" % (r["excluded_done"], r["excluded_working"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
