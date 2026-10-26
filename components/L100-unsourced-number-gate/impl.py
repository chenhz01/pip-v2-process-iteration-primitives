# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L100 无源数字拦截：报告里每个数字都要能答上「哪来的」；
答不上来的数字，进不了对外的门。逐个数字要求来源字段（文件/命令/URL）。
"""

import re

NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def gate_numbers(claims):
    """claims: [{"text": 含数字的断言, "source": 来源（文件/命令/URL）}]
    返回 {"blocked": [...被拦的 (数字, 断言) 对], "passed": 放行数, "reason": ...}
    """
    if not isinstance(claims, list):
        return {"blocked": [], "passed": 0, "reason": "输入非断言列表，无法审"}
    blocked, passed = [], 0
    for c in claims:
        if not isinstance(c, dict) or not (c.get("text") or "").strip():
            continue
        nums = NUM_RE.findall(c["text"])
        if not nums:
            passed += 1  # 没有数字的陈述无需来源
            continue
        src = (c.get("source") or "").strip()
        if not src:
            blocked.extend((n, c["text"]) for n in nums)
        else:
            passed += 1
    reason = "全部 %d 条断言数字有源（来源字段齐备），放行" % passed if not blocked \
        else "拦下 %d 个无源数字：答不上「哪来的」就不许出门" % len(blocked)
    return {"blocked": blocked, "passed": passed, "reason": reason}


def unsourced_numbers(claims):
    """只提被拦的数字清单，供改写用。"""
    return [n for n, _ in gate_numbers(claims)["blocked"]]


if __name__ == "__main__":
    report = [
        {"text": "实测 55 件组件全部跑通", "source": "run_all.py 退出码 0"},
        {"text": "通过率 92.5%，比上轮提升 3 个百分点", "source": "verify_result.json"},
        {"text": "预计下周能覆盖 80 个场景"},  # 无源
        {"text": "无数字的陈述句不需要来源", "source": ""},
    ]
    r = gate_numbers(report)
    print("审数字：%s" % r["reason"])
    for n, t in r["blocked"]:
        print("  拦截数字 %s ←「%s」" % (n, t))
    print("待补来源清单：%s" % unsourced_numbers(report))
