# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L88 退出判据先行：任务启动前校验（成功判据+失败判据+时限）三元组，缺一拒启。"""

REQUIRED = ("success_criteria", "failure_criteria", "time_limit")


def admit_task(task):
    """task: {"success_criteria":..., "failure_criteria":..., "time_limit":...}

    三元组齐 → 放行；缺任何一项（尤其失败判据）→ 拒绝开始。
    """
    missing = [k for k in REQUIRED if not task.get(k)]
    if missing:
        return {
            "admitted": False,
            "missing": missing,
            "reason": (f"缺 {'、'.join(missing)}，没有'怎样算失败/何时停'的任务不许开跑"),
        }
    return {"admitted": True, "missing": [],
            "reason": "成功判据+失败判据+时限三元组齐备，放行"}


if __name__ == "__main__":
    bad = {"success_criteria": "自测全过"}
    good = {"success_criteria": "7 件 selftest 全 PASS",
            "failure_criteria": "任一 selftest 退出码非 0 即失败回滚",
            "time_limit": "2026-10-27T18:00"}
    r1 = admit_task(bad)
    print(f"[demo1] 判了什么: 拒启={not r1['admitted']} | 为什么: {r1['reason']} | 数字: 缺项={r1['missing']}")
    r2 = admit_task(good)
    print(f"[demo2] 判了什么: 放行={r2['admitted']} | 为什么: {r2['reason']}")
