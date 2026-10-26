# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L71 断点新鲜度 — 存档放久会过期：环境指纹比对，不一致先升级存档再恢复。

L1: checkpoint 记录环境指纹（依赖版本+文件哈希），恢复时重算比对。
L2: ①指纹不一致拦截 ②一致放行。
"""

import hashlib
import json


def env_fingerprint(deps, file_hashes):
    """对 {依赖名: 版本} 与 {文件路径: 哈希} 计算确定性指纹。"""
    payload = json.dumps({"deps": dict(sorted(deps.items())),
                          "files": dict(sorted(file_hashes.items()))},
                         sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def freshness_gate(checkpoint_fp, deps, file_hashes):
    """恢复前比对存档指纹与当前环境指纹。

    返回 {"allow": bool, "stored": ..., "current": ...}
    """
    current = env_fingerprint(deps, file_hashes)
    allow = bool(checkpoint_fp) and checkpoint_fp == current
    return {"allow": allow, "stored": checkpoint_fp, "current": current,
            "action": "放行恢复" if allow else "拦截：先升级存档再恢复"}


def main():
    deps = {"pyyaml": "6.0.1", "requests": "2.31.0"}
    files = {"main.py": "aaa111", "util.py": "bbb222"}
    fp = env_fingerprint(deps, files)
    same = freshness_gate(fp, deps, files)
    changed = freshness_gate(fp, dict(deps, requests="2.32.0"), files)
    print("存档指纹=%s" % fp)
    print("环境未变: allow=%s → %s" % (same["allow"], same["action"]))
    print("requests 升级: allow=%s → %s（老存档接着用会翻车）" % (changed["allow"], changed["action"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
