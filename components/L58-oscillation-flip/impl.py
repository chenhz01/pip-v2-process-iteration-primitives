# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L58 振荡翻转检测：抓"翻烧饼"——结论在说法间来回横跳。

与 L56 的区别：L56 看动作重复，本件看结论翻转。对判定/结论序列
找长度 <=k 的周期性重复子串（如 A,B,A,B），命中 -> 振荡。
"""


def detect_oscillation(conclusions, max_period=3, min_repeats=2):
    """conclusions: 结论/判定序列（元素需可比较相等）。

    从尾端找周期 p（2<=p<=max_period）的重复：尾段满足
    seq[i]==seq[i-p] 且尾段含 >=2 种不同取值 -> 振荡。
    全相同（恒定结论）不算振荡。样本不足 2*min_repeats 才算短样本
    （5 样本 [x,y,x,y,x] 足以判定）。返回 (is_oscillating, info)，
    info 恒含 period 字段（无周期时为 None）。
    """
    n = len(conclusions)
    if n < 2 * min_repeats:
        return False, {"verdict": "SKIP", "period": None,
                       "why": "样本过短，不足以判定翻转模式"}
    for p in range(2, max_period + 1):
        tail_len = min(n, (min_repeats + 1) * p)
        seg = list(conclusions[n - tail_len:])
        if len(set(seg)) < 2:
            continue  # 恒定结论，不是翻转
        if all(seg[i] == seg[i - p] for i in range(p, len(seg))):
            return True, {"verdict": "OSCILLATING", "period": p,
                          "tail": seg,
                          "why": "尾段按周期 %d 来回翻转（%d 轮）"
                                 % (p, len(seg) // p)}
    return False, {"verdict": "STABLE", "period": None,
                   "why": "未发现周期性翻转模式"}


if __name__ == "__main__":
    _, i1 = detect_oscillation(["x", "y", "x", "y", "x"])
    print("案例1 [x,y,x,y,x] ->", i1["verdict"], "周期=%s 理由: %s"
          % (i1["period"], i1["why"]))
    _, i2 = detect_oscillation(["x", "x", "x", "y"])
    print("案例2 [x,x,x,y]   ->", i2["verdict"], "理由:", i2["why"])
    _, i3 = detect_oscillation(["x", "x", "x", "x"])
    print("案例3 [x,x,x,x]   ->", i3["verdict"], "理由:", i3["why"])
