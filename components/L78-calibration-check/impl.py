# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L78 校准体检 — 总说 90% 有把握却十次错三次，90% 就不值 90%。

L1: 收集（自报置信，实际对错）对，算校准误差（ECE 简化版），超阈出校准系数。
L2: ①高置信低正确率报过信 ②校准良好不报。
"""

ECE_THRESHOLD = 0.15  # 校准误差阈值


def _bin(conf):
    """0.0-1.0 置信划入 10 桶。"""
    return min(int(conf * 10), 9)


def calibration_check(pairs):
    """pairs: [(自报置信 0-1, 是否正确 bool)]。

    返回 {"ece": float, "overconfident": bool, "calibration_coef": float,
          "bins": [{conf, acc, n}]}
    """
    if not pairs:
        raise ValueError("至少需要一对（置信, 对错）样本")
    buckets = {}
    for conf, correct in pairs:
        if not 0.0 <= conf <= 1.0:
            raise ValueError("置信必须在 [0,1]: %r" % (conf,))
        buckets.setdefault(_bin(conf), []).append((conf, bool(correct)))
    bins, ece = [], 0.0
    for b in sorted(buckets):
        xs = buckets[b]
        n = len(xs)
        m_conf = sum(c for c, _ in xs) / n
        m_acc = sum(1 for _, ok in xs if ok) / n
        ece += n / len(pairs) * abs(m_acc - m_conf)
        bins.append({"conf": round(m_conf, 3), "acc": round(m_acc, 3), "n": n})
    overconfident = any(x["conf"] >= 0.8 and x["acc"] < x["conf"] - ECE_THRESHOLD
                        for x in bins)
    return {"ece": round(ece, 4), "overconfident": overconfident,
            "calibration_coef": round((1.0 - ece), 4), "bins": bins}


def main():
    over = calibration_check([(0.9, False)] * 3 + [(0.9, True)] + [(0.85, False)] * 2)
    good = calibration_check([(0.9, True)] * 9 + [(0.9, False)] +
                             [(0.5, True)] * 5 + [(0.5, False)] * 5)
    print("过信者: ECE=%.3f 校准系数=%.3f → %s（十次错三次那种人）"
          % (over["ece"], over["calibration_coef"],
             "报过信，打对折再信" if over["overconfident"] else "校准正常"))
    print("校准良好者: ECE=%.3f → %s" % (good["ece"],
          "报过信" if good["overconfident"] else "不报，置信可信"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
