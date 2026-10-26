# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L66 重放等价 — 同一段操作重跑结果应一样；不一样说明有东西在暗地里变了。

L1: 记录首次执行的输入/输出指纹（规范化 JSON + SHA-256），重放比对；
    不一致时定位差异在输入侧还是输出侧（输出侧漂移 = 疑似未固定随机源/隐藏状态）。
"""
import hashlib
import json


def fingerprint(obj) -> str:
    """规范化 JSON + SHA-256，得到稳定指纹（前 16 位十六进制）。"""
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]


def record(input_data, output_data) -> dict:
    """首跑登记：留输入/输出指纹。"""
    return {"input_fp": fingerprint(input_data), "output_fp": fingerprint(output_data)}


def verify(recorded: dict, replayed_input, replayed_output) -> dict:
    """重放比对。返回 {"verdict","cause","detail"}。
    输入指纹一致而输出指纹漂移 → 判定存在未固定的非确定性来源。"""
    in_fp = fingerprint(replayed_input)
    out_fp = fingerprint(replayed_output)
    if in_fp != recorded["input_fp"]:
        return {"verdict": "FAIL", "cause": "input-drift",
                "detail": f"输入变了 {recorded['input_fp']} -> {in_fp}"}
    if out_fp != recorded["output_fp"]:
        return {"verdict": "FAIL", "cause": "output-drift",
                "detail": f"输入未变但输出漂移 {recorded['output_fp']} -> {out_fp}"
                          "（疑似未固定随机源/隐藏状态）"}
    return {"verdict": "PASS", "cause": None, "detail": "重放一致"}


if __name__ == "__main__":
    def pure(x):
        return {"sq": x * x}

    rec = record({"x": 7}, pure(7))
    r1 = verify(rec, {"x": 7}, pure(7))
    print(f"[纯函数重放] 判定={r1['verdict']} 原因={r1['cause']} —— 两次指纹均 {rec['output_fp']}")

    rec2 = record({"x": 7}, {"sq": 49, "rand": 0.5341})
    r2 = verify(rec2, {"x": 7}, {"sq": 49, "rand": 0.9823})
    print(f"[未固定随机重放] 判定={r2['verdict']} 原因={r2['cause']} —— {r2['detail']}")
