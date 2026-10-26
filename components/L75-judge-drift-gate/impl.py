# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L75 评审器漂移门 — 打分的人会越打越松或越打越严，变了先校准再信。

L1: 对评审分数序列做分布检验（均值漂移/方差膨胀），超阈判漂移，暂停采信。
L2: ①分数整体上移 2σ 报漂移 ②平稳不报。
"""

SHIFT_SIGMA = 2.0   # 均值漂移显著性阈值（基线标准差的倍数）
VAR_RATIO = 4.0     # 方差膨胀阈值（近期方差 > 4 倍基线方差）


def _mean(xs):
    return sum(xs) / len(xs)


def _std(xs):
    m = _mean(xs)
    return (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5


def drift_gate(baseline_scores, recent_scores):
    """baseline_scores: 校准期分数；recent_scores: 近期分数。

    返回 {"drift": bool, "mean_shift_sigma": float, "var_ratio": float,
          "reasons": [...]}
    """
    if len(baseline_scores) < 2 or len(recent_scores) < 2:
        raise ValueError("两段序列各至少 2 个样本才能做分布检验")
    b_std, b_mean = _std(baseline_scores), _mean(baseline_scores)
    r_mean, r_var = _mean(recent_scores), _std(recent_scores) ** 2
    b_var = b_std ** 2
    shift_sigma = (r_mean - b_mean) / b_std if b_std > 0 else float("inf")
    var_ratio = r_var / b_var if b_var > 0 else float("inf")
    reasons = []
    if shift_sigma > SHIFT_SIGMA:
        reasons.append("均值上移 %.2fσ（>%.1fσ）" % (shift_sigma, SHIFT_SIGMA))
    if var_ratio > VAR_RATIO:
        reasons.append("方差膨胀 %.1f 倍（>%.1f 倍）" % (var_ratio, VAR_RATIO))
    return {"drift": bool(reasons), "mean_shift_sigma": round(shift_sigma, 3),
            "var_ratio": round(var_ratio, 3), "reasons": reasons}


def main():
    stable_b = [3.0, 3.1, 2.9, 3.0, 3.0, 3.1, 2.9, 3.0]
    stable_r = [3.0, 3.1, 3.0, 2.9]
    loose_r = [3.6, 3.7, 3.8, 3.7]
    wild_r = [1.0, 5.0, 1.5, 4.5]
    a = drift_gate(stable_b, stable_r)
    b = drift_gate(stable_b, loose_r)
    c = drift_gate(stable_b, wild_r)
    print("平稳期: drift=%s (σ漂移=%.2f, 方差比=%.2f) → 继续采信" % (a["drift"], a["mean_shift_sigma"], a["var_ratio"]))
    print("越打越松: drift=%s reasons=%s → 暂停采信，先校准" % (b["drift"], b["reasons"]))
    print("忽高忽低: drift=%s reasons=%s → 打分标准失稳" % (c["drift"], c["reasons"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
