# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L106 结果新鲜度 — 工具返回的数据要贴"何时采的"标签。

L1：为工具结果打时间戳，消费方校验年龄 vs 该数据类型的保鲜期（TTL），
    过期拒用；时间戳在未来（时钟漂移/伪造）同样拒用。
"""


def check_freshness(collected_at, now, ttl_seconds, data_type="generic"):
    """校验工具结果年龄。collected_at/now 用 Unix 秒，全部显式传入（确定性）。"""
    age = now - collected_at
    if age < 0:
        return {"verdict": "REJECT", "age_seconds": age, "ttl_seconds": ttl_seconds,
                "reason": "时间戳在未来（age=%ds）：时钟漂移或伪造，一律拒用" % age}
    if age > ttl_seconds:
        return {"verdict": "REJECT", "age_seconds": age, "ttl_seconds": ttl_seconds,
                "reason": "已过期：数据类型 %s 保鲜期 %ds，实际年龄 %ds（超 %ds）"
                          % (data_type, ttl_seconds, age, age - ttl_seconds)}
    return {"verdict": "USE", "age_seconds": age, "ttl_seconds": ttl_seconds,
            "reason": "新鲜：年龄 %ds ≤ 保鲜期 %ds（余量 %ds）"
                      % (age, ttl_seconds, ttl_seconds - age)}


if __name__ == "__main__":
    NOW = 1769472000
    r1 = check_freshness(NOW - 3, NOW, 10, "stock_price")
    r2 = check_freshness(NOW - 3 * 86400, NOW, 10, "stock_price")
    r3 = check_freshness(NOW + 60, NOW, 10, "stock_price")
    print("[1] 3秒前的股价   -> %s | %s" % (r1["verdict"], r1["reason"]))
    print("[2] 3天前的股价   -> %s | %s" % (r2["verdict"], r2["reason"]))
    print("[3] 未来时间戳    -> %s | %s" % (r3["verdict"], r3["reason"]))
