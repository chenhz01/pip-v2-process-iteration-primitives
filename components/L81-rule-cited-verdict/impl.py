# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L81 规则引用判定 — 审查结论必须指出"违反了哪一条规定、原文是什么"。

L1: 校验每条结论含（规则 ID + 原文引用 + 修复建议）三件套，缺一判无效。
"""
REQUIRED = ("rule_id", "quote", "fix")


def validate(verdict: dict) -> dict:
    """单条结论校验：三件套任一缺失/为空 → 判无效并列缺失项。"""
    missing = [k for k in REQUIRED
               if not (isinstance(verdict.get(k), str) and verdict.get(k).strip())]
    return {"valid": not missing, "missing": missing, "rule_id": verdict.get("rule_id")}


def validate_batch(verdicts) -> dict:
    """批量校验：返回整体有效性与无效条目定位。"""
    results = [validate(v) for v in verdicts]
    bad = [i for i, r in enumerate(results) if not r["valid"]]
    return {"all_valid": not bad, "invalid_indexes": bad, "results": results}


if __name__ == "__main__":
    good = {"rule_id": "R-102", "quote": "所有外发产物不得包含内部路径",
            "fix": "将内部路径替换为占位符后再发布"}
    bad = {"rule_id": "R-107", "fix": "补充来源标注"}
    r1, r2 = validate(good), validate(bad)
    print(f"[三件套齐] 有效={r1['valid']} 缺失={r1['missing']}")
    print(f"[缺原文引用] 有效={r2['valid']} 缺失={r2['missing']} → 该结论不算数")
