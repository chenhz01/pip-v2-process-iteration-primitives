# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L80 行为漂移门 — 提示词没改，模型行为也可能悄悄变；固定题库定期抽查。

L1: 固定探针题库周期重跑，输出行为指纹哈希序列；哈希变化 → 漂移警报。
"""
import hashlib
import json

PROBE_BANK = ("解释什么是幂等性", "写一个冒泡排序", "总结一段话的要点")


def normalize(resp: str) -> str:
    """规范化（去空白+小写）：字面微调不触发，实质内容变化才触发。"""
    return "".join(resp.split()).lower()


def behavior_fingerprint(responses) -> str:
    """整份题库回答 → 行为指纹（规范化后 SHA-256，前 16 位）。"""
    canon = json.dumps([normalize(r) for r in responses], ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def gate(history, current_fp) -> dict:
    """history: 以往指纹序列（旧→新）；当前指纹与上一枚比对。"""
    last = history[-1] if history else None
    changed = last is not None and current_fp != last
    return {"verdict": "DRIFT-ALERT" if changed else "STABLE",
            "last_fp": last, "current_fp": current_fp}


if __name__ == "__main__":
    baseline = ["幂等性指同一操作执行多次与一次效果相同",
                "def bubble(a): ... 时间复杂度 O(n^2)",
                "本段主旨是……"]
    fp1 = behavior_fingerprint(baseline)
    g1 = gate([fp1], fp1)
    print(f"[抽查#2 与上次指纹一致] 判定={g1['verdict']} 指纹={fp1}")
    drifted = ["幂等性指同一操作执行多次与一次效果相同",
               "冒泡排序大概就是两两交换吧，别的记不清了",
               "本段主旨是……"]
    fp2 = behavior_fingerprint(drifted)
    g2 = gate([fp1], fp2)
    print(f"[抽查#3 指纹变化] 判定={g2['verdict']} {g2['last_fp']} -> {g2['current_fp']} → 先查原因再采信")
