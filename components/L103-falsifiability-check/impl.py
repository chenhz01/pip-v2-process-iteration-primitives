# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L103 可证伪化：结论必须附带「什么证据会推翻我」，否则降级为假说。"""


def run(conclusions):
    """conclusions: [{"claim": str, "falsifier": str | None}]
    返回逐条：CONCLUSION（附可伪条件，保留结论级）/ HYPOTHESIS（无可伪条件，降级）。
    """
    if not isinstance(conclusions, list):
        raise TypeError("conclusions 必须是列表")
    rows, kept = [], 0
    for c in conclusions:
        claim = (c.get("claim") or "").strip()
        f = (c.get("falsifier") or "").strip()
        if not claim:
            rows.append({"claim": "", "verdict": "INVALID", "why": "结论文本为空"})
            continue
        if not f:
            rows.append({"claim": claim, "verdict": "HYPOTHESIS",
                         "why": "无可伪条件：答不上「什么证据会推翻我」，只是口号"})
            continue
        rows.append({"claim": claim, "verdict": "CONCLUSION",
                     "why": "可伪条件在案：%s" % f[:40]})
        kept += 1
    return {"rows": rows, "conclusions": kept, "hypotheses": len(rows) - kept,
            "total": len(conclusions)}


if __name__ == "__main__":
    demo = run([
        {"claim": "55 件 v2 全部可独立运行", "falsifier": "任一件 selftest 退出码非 0"},
        {"claim": "本轮日跑比上轮更快"},
    ])
    for r in demo["rows"]:
        print("%-11s %s | %s" % (r["verdict"], r["claim"][:24], r["why"]))
    print("结论 %d 条 / 降级假说 %d 条 / 共 %d 条"
          % (demo["conclusions"], demo["hypotheses"], demo["total"]))
