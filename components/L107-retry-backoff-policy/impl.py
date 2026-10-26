# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L107 重试退避策略 — 失败了别立刻疯狂重试，把对方打得更死。

L1：校验重试间隔序列满足指数退避 + 上限：
    ① 不许出现零间隔（连击）；② 序列须非降且逐级按比率放大；
    ③ 单级不超过单次上限；④ 总次数封顶。违规即拦截。
"""


def check_backoff(intervals, max_retries=6, base=1.0, ratio=2.0, cap=60.0):
    """intervals: 各次重试前等待秒数序列。返回裁决 + 违规清单。"""
    violations = []
    if len(intervals) > max_retries:
        violations.append("总次数 %d 超封顶 %d" % (len(intervals), max_retries))
    for i, iv in enumerate(intervals):
        if iv <= 0:
            violations.append("第%d次重试间隔 %.1fs：零间隔连击" % (i + 1, iv))
            continue
        if iv > cap:
            violations.append("第%d次重试间隔 %.1fs 超单级上限 %.0fs" % (i + 1, iv, cap))
        if i > 0 and intervals[i - 1] > 0 and iv < intervals[i - 1] * ratio:
            violations.append("第%d次重试间隔 %.1fs 未达指数退避（需≥%.1fs）"
                              % (i + 1, iv, intervals[i - 1] * ratio))
    return {"verdict": "VIOLATED" if violations else "COMPLIANT",
            "intervals": list(intervals), "violations": violations}


if __name__ == "__main__":
    cases = [("零间隔连击", [0, 0, 0]),
             ("合规指数退避", [1.0, 2.0, 4.0, 8.0]),
             ("越等越短(反向)", [8.0, 4.0, 2.0]),
             ("次数超封顶", [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0])]
    for name, iv in cases:
        r = check_backoff(iv)
        print("[%s] %s -> %s" % (name, r["verdict"], "; ".join(r["violations"]) or "满足退避+上限"))
