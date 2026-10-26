# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L85 selftest：对齐卡片 L2 断言 ①矛盾未裁决拒绝写入 ②裁决后写入并记录理由。"""

from impl import write_memory

# 断言①：同 key 不同 value 且无裁决 → 拒写
mem = [{"key": "owner", "value": "alice"}]
r1 = write_memory({"key": "owner", "value": "bob"}, mem)
assert r1["written"] is False, f"矛盾未裁决应拒绝写入, got {r1}"
assert r1["conflicts"], "应列出矛盾对"

# 断言②：裁决后写入，且理由被记录
r2 = write_memory({"key": "owner", "value": "bob"}, mem,
                  verdict={"decision": "overwrite", "reason": "alice 已转岗"})
assert r2["written"] is True, f"裁决后应写入, got {r2}"
assert mem[-1]["verdict"]["reason"] == "alice 已转岗", "裁决理由应随记忆落盘"

# 无矛盾直接写不受闸
r3 = write_memory({"key": "lang", "value": "zh"}, mem)
assert r3["written"] is True

print("PASS")
