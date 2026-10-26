# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L106 selftest — 对齐卡片 L2 两条断言。"""
import impl

NOW = 1769472000

# 断言①：过期数据拒用（3 天前的股价，TTL 10 秒 → REJECT）
r1 = impl.check_freshness(NOW - 3 * 86400, NOW, 10, "stock_price")
assert r1["verdict"] == "REJECT", "过期数据必须拒用"
assert r1["age_seconds"] == 3 * 86400, "年龄计算必须准确（259200s）"

# 断言②：新鲜放行（3 秒前的股价，TTL 10 秒 → USE）
r2 = impl.check_freshness(NOW - 3, NOW, 10, "stock_price")
assert r2["verdict"] == "USE", "新鲜数据应放行"
assert r2["age_seconds"] == 3, "年龄计算必须准确（3s）"

# 负对照①：时间戳在未来 → 拒用（时钟漂移/伪造）
r3 = impl.check_freshness(NOW + 60, NOW, 10)
assert r3["verdict"] == "REJECT", "未来时间戳必须拒用"

# 负对照②：恰好压线（age == ttl）不算过期，放行
r4 = impl.check_freshness(NOW - 10, NOW, 10)
assert r4["verdict"] == "USE", "age==ttl 为边界，应放行不误杀"

print("PASS L106: 过期拒用(断言①) / 新鲜放行(断言②) / 未来戳负对照 / 压线边界 共4断言全过")
