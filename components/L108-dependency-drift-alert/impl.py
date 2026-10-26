# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L108 依赖漂移警报 — 上周能跑的程序这周跑不动，多半是环境里有人换了东西。

L1：记录依赖清单哈希，定期比对；差异 → 列出增/删/改并评估影响面
    （改动项在"关键依赖"名单中 → 高影响）。
"""
import hashlib
import json


def lock_hash(lock):
    """依赖清单快照哈希（键排序规范化）。lock: {name: version}"""
    canon = json.dumps(lock, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def diff_dependencies(old_lock, new_lock, critical=()):
    """对比两份依赖清单，列增/删/改 + 影响面评估。"""
    added = sorted(set(new_lock) - set(old_lock))
    removed = sorted(set(old_lock) - set(new_lock))
    changed = {k: (old_lock[k], new_lock[k]) for k in sorted(set(old_lock) & set(new_lock))
               if old_lock[k] != new_lock[k]}
    changed = {k: list(v) for k, v in changed.items()}
    impact = sorted({k for k in list(changed) + added if k in critical})
    return {"verdict": "ALERT" if (added or removed or changed) else "QUIET",
            "old_hash": lock_hash(old_lock), "new_hash": lock_hash(new_lock),
            "added": added, "removed": removed, "changed": changed,
            "high_impact": impact}


if __name__ == "__main__":
    last_week = {"requests": "2.31.0", "pydantic": "2.5.0", "numpy": "1.26.0"}
    this_week = {"requests": "2.32.0", "pydantic": "2.5.0", "numpy": "2.0.0", "uvloop": "0.19.0"}
    r = diff_dependencies(last_week, this_week, critical={"numpy", "pydantic"})
    print("[1] 漂移判定: %s | 清单哈希 %s -> %s" % (r["verdict"], r["old_hash"], r["new_hash"]))
    for k, (a, b) in r["changed"].items():
        print("    改动: %s %s -> %s%s" % (k, a, b, "  [高影响:关键依赖]" if k in r["high_impact"] else ""))
    for k in r["added"]:
        print("    新增: %s" % k)
    r2 = diff_dependencies(last_week, dict(last_week))
    print("[2] 无变化判定: %s | 差异 0 | 哈希 %s（不变）" % (r2["verdict"], r2["new_hash"]))
