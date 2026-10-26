# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L102 负对照强制：验收判据必须附带「故意做错」的负对照并确认真能拦住。

没有负对照的判据降级为 UNQUALIFIED——先证明尺子能拦废话，再拿它量真话。
"""


def run(criteria):
    """criteria: [{"criterion": str, "negative_control": {"case": str, "blocked": bool} | None}]
    返回逐条判定：QUALIFIED（有负对照且拦截成功）/ UNQUALIFIED（无负对照或没拦住）。
    """
    if not isinstance(criteria, list):
        raise TypeError("criteria 必须是列表")
    rows, qualified = [], 0
    for c in criteria:
        crit = (c.get("criterion") or "").strip()
        nc = c.get("negative_control")
        if not crit:
            rows.append({"criterion": "", "verdict": "UNQUALIFIED", "why": "判据文本为空"})
            continue
        if not isinstance(nc, dict) or not (nc.get("case") or "").strip():
            rows.append({"criterion": crit, "verdict": "UNQUALIFIED",
                         "why": "无负对照：尺子没证明自己能拦住做错的东西"})
            continue
        if nc.get("blocked") is not True:
            rows.append({"criterion": crit, "verdict": "UNQUALIFIED",
                         "why": "负对照未被拦截（blocked≠True）：判据是漏的"})
            continue
        rows.append({"criterion": crit, "verdict": "QUALIFIED", "why": "负对照存在且拦截成功"})
        qualified += 1
    rate = qualified / len(criteria) if criteria else 0.0
    return {"rows": rows, "qualified": qualified, "total": len(criteria),
            "qualified_rate": round(rate, 3),
            "verdict": "PASS" if criteria and qualified == len(criteria) else "CRITERIA-NOT-READY"}


if __name__ == "__main__":
    demo = run([
        {"criterion": "所有仓必须含 tag v1.0",
         "negative_control": {"case": "建一个无 tag 的仓喂给核验器", "blocked": True}},
        {"criterion": "所有输出必须非空"},
        {"criterion": "数字必须带来源",
         "negative_control": {"case": "混入一条无源数字", "blocked": False}},
    ])
    for r in demo["rows"]:
        print("%-14s %s | %s" % (r["verdict"], r["criterion"][:24] or "(空)", r["why"]))
    print("判据可用率 %d/%d → %s" % (demo["qualified"], demo["total"], demo["verdict"]))
