# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L67 副作用清单前置 — 动手之前先列"这步会动到哪些东西"：文件、网络、钱、别人。

L1: 执行前强制产出副作用清单（对象/可逆性/影响面）；
    清单缺失或含未声明副作用 → 拦；含「不可逆」项时要求二次确认标记。
"""


def check(manifest, actual_effects=(), confirmed=False) -> dict:
    """manifest: None 或 [{"target","reversibility","impact"}]；
    actual_effects: 实际会触碰的对象，用于对账未声明副作用；
    confirmed: 针对不可逆项的二次确认标记。
    返回 {"verdict","reasons","need_confirm"}。"""
    if not manifest:
        return {"verdict": "BLOCK", "need_confirm": False,
                "reasons": ["无副作用清单——先列出对象/可逆性/影响面再执行"]}
    reasons, declared = [], set()
    for i, item in enumerate(manifest):
        if not all(str(item.get(k, "")).strip() for k in ("target", "reversibility", "impact")):
            reasons.append(f"第{i}项字段不全（需 target/reversibility/impact）")
        declared.add(item.get("target"))
    for eff in actual_effects:
        if eff not in declared:
            reasons.append(f"未声明副作用: {eff}")
    irreversible = [m.get("target") for m in manifest if m.get("reversibility") == "irreversible"]
    need_confirm = bool(irreversible)
    if need_confirm and not confirmed:
        reasons.append(f"含不可逆项 {irreversible}，需二次确认标记")
    return {"verdict": "BLOCK" if reasons else "PASS",
            "reasons": reasons, "need_confirm": need_confirm}


if __name__ == "__main__":
    r1 = check(None)
    print(f"[无清单] 判定={r1['verdict']} —— {r1['reasons'][0]}")
    m = [{"target": "draft.md", "reversibility": "reversible", "impact": "单文件"},
         {"target": "prod-db.users", "reversibility": "irreversible", "impact": "全量用户表"}]
    r2 = check(m, actual_effects=("draft.md",), confirmed=False)
    print(f"[含不可逆+未确认] 判定={r2['verdict']} 需二次确认={r2['need_confirm']} —— {r2['reasons']}")
    r3 = check(m, actual_effects=("draft.md",), confirmed=True)
    print(f"[含不可逆+已确认] 判定={r3['verdict']} 需二次确认={r3['need_confirm']}")
    r4 = check([{"target": "a.txt", "reversibility": "reversible", "impact": "单文件"}],
               actual_effects=("a.txt", "b.txt"))
    print(f"[未声明副作用] 判定={r4['verdict']} —— {r4['reasons']}")
