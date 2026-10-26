# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L83 双阈值充足度 — 上下文太多太少都坏：给"信息够不够"设上下两条线，越线都报警。

L1: 量化关键信息覆盖度，双阈值判定：超上阈（溢出）→ 压缩；低于下阈（不足）→ 补料。
"""
UPPER, LOWER = 0.9, 0.3


def estimate_coverage(context: str, key_items) -> float:
    """关键信息条目在上下文中的命中率（0..1）。"""
    if not key_items:
        return 0.0
    return sum(1 for k in key_items if k in context) / len(key_items)


def assess(coverage: float, upper=UPPER, lower=LOWER) -> dict:
    """双阈值判定：>upper 报压缩，<lower 报补料，居中维持。"""
    if coverage > upper:
        verdict, action = "OVERFLOW", "压缩：信息过饱和，删冗余腾窗口"
    elif coverage < lower:
        verdict, action = "INSUFFICIENT", "补料：关键信息覆盖不足，回检索补齐"
    else:
        verdict, action = "OK", "维持当前上下文"
    return {"verdict": verdict, "action": action, "coverage": round(coverage, 3),
            "upper": upper, "lower": lower}


if __name__ == "__main__":
    keys = ["预算 5 万", "截止 11 月 1 日", "负责人张三", "验收标准"]
    r1 = assess(1.0)
    print(f"[覆盖度 1.0 > 上阈 0.9] 判定={r1['verdict']} 动作={r1['action']}")
    c2 = estimate_coverage("只有一句寒暄，没有实质内容", keys)
    r2 = assess(c2)
    print(f"[覆盖度 {r2['coverage']} < 下阈 0.3] 判定={r2['verdict']} 动作={r2['action']}")
    r3 = assess(0.5)
    print(f"[覆盖度 0.5 居中] 判定={r3['verdict']} 动作={r3['action']}")
