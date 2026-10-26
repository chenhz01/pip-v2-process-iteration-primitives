# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L104 契约漂移检测 — 工具的说明书会悄悄变，调用前先对指纹。

L1：缓存工具 schema 指纹，调用前比对；漂移 → 逐项列差异并标记受影响调用点。
判定只看 schema 结构（参数名/类型/必填、返回字段），不看语义。
"""
import hashlib
import json


def fingerprint(schema):
    """规范化（键排序）后取 16 位 SHA-256 指纹，避免键顺序差异误报。"""
    canon = json.dumps(schema, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def diff_schema(old, new):
    """逐层列差异：参数增/删/改 + 返回字段增/删。"""
    diffs = []
    op, np = old.get("params", {}), new.get("params", {})
    for k in sorted(set(op) | set(np)):
        if k not in op:
            diffs.append("params.%s: 新增" % k)
        elif k not in np:
            diffs.append("params.%s: 删除" % k)
        elif op[k] != np[k]:
            diffs.append("params.%s: %r -> %r" % (k, op[k], np[k]))
    ro, rn = old.get("returns", []), new.get("returns", [])
    for f in sorted(set(ro) | set(rn)):
        if f not in ro:
            diffs.append("returns.%s: 新增字段" % f)
        elif f not in rn:
            diffs.append("returns.%s: 缺失字段" % f)
    return diffs


def check_contract_drift(cached, current, call_sites=None):
    """调用前比对缓存 schema；漂移 → BLOCK 并列差异、标受影响调用点。"""
    fp_old, fp_new = fingerprint(cached), fingerprint(current)
    if fp_old == fp_new:
        return {"verdict": "PASS", "drift": False, "diffs": [], "fingerprint": fp_new}
    diffs = diff_schema(cached, current)
    affected = [c["name"] for c in (call_sites or [])
                if c.get("tool") == current.get("name")]
    return {"verdict": "BLOCK", "drift": True, "diffs": diffs,
            "fingerprint": "%s -> %s" % (fp_old, fp_new),
            "affected_calls": affected}


if __name__ == "__main__":
    cached = {"name": "get_weather", "params": {"city": "str", "unit": "str"}, "returns": ["temp", "desc"]}
    drifted = {"name": "get_weather", "params": {"location": "str", "unit": "str"}, "returns": ["temp", "desc", "humidity"]}
    calls = [{"name": "查北京天气", "tool": "get_weather"}]
    r1 = check_contract_drift(cached, drifted, calls)
    print("[1] 漂移判定: %s | 指纹 %s" % (r1["verdict"], r1["fingerprint"]))
    for d in r1["diffs"]:
        print("    差异: %s" % d)
    print("    受影响调用点: %s" % r1["affected_calls"])
    r2 = check_contract_drift(cached, dict(cached))
    print("[2] 一致判定: %s | 差异数 %d | 指纹 %s" % (r2["verdict"], len(r2["diffs"]), r2["fingerprint"]))
