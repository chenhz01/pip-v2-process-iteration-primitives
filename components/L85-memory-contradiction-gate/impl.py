# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L85 矛盾裁决门：新记忆与旧记忆打架时，写入前必须显式裁决，未裁决拒写。"""


def find_contradictions(record, existing):
    """矛盾判定：同 key 不同 value。返回矛盾对列表。"""
    conflicts = []
    for old in existing:
        if old.get("key") == record.get("key") and old.get("value") != record.get("value"):
            conflicts.append({"old": old["value"], "new": record["value"]})
    return conflicts


def write_memory(record, existing, verdict=None):
    """写入闸：发现矛盾对且未裁决 → 拒写；裁决后写入并记录理由。

    verdict: {"decision": "overwrite"|"coexist"|"discard", "reason": str}
    """
    conflicts = find_contradictions(record, existing)
    if conflicts and not verdict:
        return {
            "written": False,
            "reason": f"发现 {len(conflicts)} 对矛盾且未裁决，拒绝写入",
            "conflicts": conflicts,
        }
    if conflicts and verdict.get("decision") not in ("overwrite", "coexist", "discard"):
        return {"written": False, "reason": "裁决结果非法（须 overwrite/coexist/discard）",
                "conflicts": conflicts}
    if conflicts and verdict.get("decision") == "discard":
        return {"written": False, "reason": f"已裁决丢弃: {verdict.get('reason')}",
                "conflicts": conflicts}
    entry = dict(record)
    if conflicts:
        entry["verdict"] = verdict
    existing.append(entry)
    return {"written": True, "reason": "写入成功" if not conflicts
            else f"裁决后写入，理由: {verdict.get('reason')}", "conflicts": conflicts}


if __name__ == "__main__":
    mem = [{"key": "deploy_branch", "value": "main"}]
    new = {"key": "deploy_branch", "value": "release/2.0"}
    r1 = write_memory(new, mem)
    print(f"[demo1] 判了什么: 拒写={not r1['written']} | 为什么: {r1['reason']} | 数字: 矛盾对={len(r1['conflicts'])}")
    r2 = write_memory(new, mem, verdict={"decision": "overwrite", "reason": "2.0 已灰度接管"})
    print(f"[demo2] 判了什么: 写入={r2['written']} | 为什么: {r2['reason']} | 数字: 记忆数={len(mem)}")
