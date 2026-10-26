# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L99 确定性复验：号称「每次都一样」的代码，连跑两次必须一字不差；
差一个字，就摘掉确定性标记。输出逐字节比对，不一致 → 撤销标记。
"""


def recheck_determinism(step_name, run_fn):
    """对标记为确定性的步骤连跑 2 次，逐字节比对输出。
    run_fn 无参调用两次（调用方保证其内部确定）。返回 (keep_flag, detail)。
    """
    a = run_fn()
    b = run_fn()
    if a != b:
        diff_at = next((i for i, (x, y) in enumerate(zip(str(a), str(b))) if x != y), None)
        return False, {
            "step": step_name,
            "verdict": "REVOKE",
            "reason": "两次输出不一致（首个差异字符位 %s）：摘掉确定性标记" % diff_at,
            "out_a": a, "out_b": b,
        }
    return True, {
        "step": step_name,
        "verdict": "KEEP",
        "reason": "两次输出逐字节一致（%d 字节），确定性标记保留" % len(str(a)),
        "out_a": a, "out_b": b,
    }


def stable_step():
    """真·确定性：纯函数。"""
    return "sha:41b9c8" + "|rows=128"


def tainted_step():
    """伪确定性：内部藏着会变的东西（用可变闭包状态模拟，不用随机也出得来）。"""
    if not hasattr(tainted_step, "n"):
        tainted_step.n = 0
    tainted_step.n += 1
    return "sha:41b9c8|rows=128|run=%d" % tainted_step.n


if __name__ == "__main__":
    keep, d = recheck_determinism("纯函数步骤", stable_step)
    print("复验[纯函数] %s —— %s" % (d["verdict"], d["reason"]))
    keep2, d2 = recheck_determinism("藏状态步骤", tainted_step)
    print("复验[藏状态] %s —— %s" % (d2["verdict"], d2["reason"]))
    if d2.get("out_a"):
        print("  out_a=%r" % d2["out_a"])
        print("  out_b=%r" % d2["out_b"])
