# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L84 相关性邻接度：量化相关信息在上下文中的分散度，超阈建议重组而非压缩。"""

DISPERSION_THRESHOLD = 0.5


def relevance_adjacency(total_len, relevant_positions, threshold=DISPERSION_THRESHOLD):
    """按关键块间距/总长算分散度，超阈建议重组（不是压缩）。

    relevant_positions: 相关块的索引/位置列表；total_len: 上下文总长。
    分散度 = (最远两块间距) / 总长。
    """
    if total_len <= 0 or len(relevant_positions) < 2:
        return {"verdict": "ok", "dispersion": 0.0,
                "reason": "相关块不足两块或上下文为空，无需处理"}
    positions = sorted(relevant_positions)
    dispersion = (positions[-1] - positions[0]) / total_len
    if dispersion > threshold:
        return {
            "verdict": "reorganize",
            "dispersion": round(dispersion, 3),
            "threshold": threshold,
            "reason": (f"相关块分散度 {dispersion:.2f} 超阈 {threshold}，"
                       "答案被拉太远，建议重组信息位置而非压缩"),
        }
    return {"verdict": "ok", "dispersion": round(dispersion, 3),
            "threshold": threshold, "reason": "相关块集中，不报"}


if __name__ == "__main__":
    n = 100
    # 头尾各一块，中间隔 95：高分散
    a = relevance_adjacency(n, [2, 3, 97])
    print(f"[demo1] 判了什么: {a['verdict']} | 为什么: {a['reason']} | 数字: 分散度={a['dispersion']}")
    # 三块挤在一起：集中
    b = relevance_adjacency(n, [10, 12, 15])
    print(f"[demo2] 判了什么: {b['verdict']} | 为什么: {b['reason']} | 数字: 分散度={b['dispersion']}")
