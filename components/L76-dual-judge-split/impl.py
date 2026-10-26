# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L76 双评审分歧 — 分歧太大说明标准不清或有人在瞎打，先解决再谈分数。

L1: 双评审逐维度打分，分差>阈 → 输出分歧定位（逐维度）+ 强制第三次仲裁。
L2: ①分差超阈触发仲裁 ②一致直接过。
"""

SPLIT_THRESHOLD = 2.0  # 单维度分差阈值（0-10 分制）


def split_check(judge_a, judge_b):
    """judge_a/judge_b: {维度: 分数}。

    返回 {"agree": bool, "arbitrate": bool, "total_gap": float,
          "dimensions": {维度: {"a":, "b":, "gap":, "flag":}}}
    """
    if not isinstance(judge_a, dict) or not isinstance(judge_b, dict):
        raise ValueError("评审分必须是 {维度: 分数} 字典")
    if set(judge_a) != set(judge_b):
        raise ValueError("两位评审必须评同一组维度: %r vs %r" % (sorted(judge_a), sorted(judge_b)))
    dims = {}
    for k in sorted(judge_a):
        gap = abs(judge_a[k] - judge_b[k])
        dims[k] = {"a": judge_a[k], "b": judge_b[k], "gap": round(gap, 3),
                   "flag": gap > SPLIT_THRESHOLD}
    total_gap = round(sum(judge_a[k] - judge_b[k] for k in judge_a), 3)
    arbitrate = any(d["flag"] for d in dims.values())
    return {"agree": not arbitrate, "arbitrate": arbitrate,
            "total_gap": total_gap, "dimensions": dims}


def main():
    a = {"正确性": 9, "完整性": 8, "风格": 7}
    b_ok = {"正确性": 9, "完整性": 8, "风格": 8}
    b_bad = {"正确性": 9, "完整性": 4, "风格": 7}
    ra = split_check(a, b_ok)
    rb = split_check(a, b_bad)
    print("一致情形: agree=%s → 直接采信，无需仲裁" % ra["agree"])
    print("分歧情形: agree=%s 总分差=%s → 强制第三次仲裁" % (rb["agree"], rb["total_gap"]))
    for k, d in rb["dimensions"].items():
        print("  维度[%s]: a=%s b=%s gap=%s %s" %
              (k, d["a"], d["b"], d["gap"], "← 分歧点" if d["flag"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
