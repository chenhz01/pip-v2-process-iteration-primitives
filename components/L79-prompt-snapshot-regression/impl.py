# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L79 快照回归 — 改提示词前先给老提示词拍快照、存典型回答特征；改完重放比对。

L1: 维护（输入→期望特征）快照集，改版后重放比对特征（不比对字面），漂移列出。
"""
import re


def extract_features(response: str) -> dict:
    """从回答提取行为特征（结构特征而非字面全文）。"""
    return {
        "lang_zh": bool(re.search(r"[\u4e00-\u9fff]", response)),
        "has_code": "```" in response,
        "has_list": bool(re.search(r"(?m)^\s*(?:[-*]|\d+\.)", response)),
        "len_bucket": ("short" if len(response) < 80
                       else "mid" if len(response) < 400 else "long"),
    }


def check(snapshot: dict, new_response: str) -> dict:
    """snapshot: {"input": str, "expected": {特征: 值}}；重放并比对关键特征。"""
    got = extract_features(new_response)
    drift = {k: {"expected": v, "got": got.get(k, "<missing>")}
             for k, v in snapshot.get("expected", {}).items() if got.get(k) != v}
    return {"verdict": "REGRESSION" if drift else "PASS",
            "input": snapshot.get("input"), "drift": drift, "features": got}


if __name__ == "__main__":
    snap = {"input": "用 Python 写快排",
            "expected": {"lang_zh": True, "has_code": True, "has_list": False}}
    old = "好的，下面是快排实现：\n```python\ndef qs(a): ...\n```\n如有疑问请追问。"
    r1 = check(snap, old)
    print(f"[改版前基线重放] 判定={r1['verdict']} 漂移数={len(r1['drift'])}")
    new = "Sure, here is quicksort:\n```python\ndef qs(a): ...\n```"
    r2 = check(snap, new)
    print(f"[改版后重放] 判定={r2['verdict']} 漂移={r2['drift']}")
