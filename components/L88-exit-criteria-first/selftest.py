# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L88 selftest：对齐卡片 L2 断言 ①缺失败判据拒启 ②三元组齐放行。"""

from impl import admit_task

# 断言①：只有成功判据，缺失败判据与时限 → 拒绝启动
r1 = admit_task({"success_criteria": "跑通即可"})
assert r1["admitted"] is False, f"缺失败判据应拒启, got {r1}"
assert "failure_criteria" in r1["missing"], "缺失清单应包含 failure_criteria"

# 只缺失败判据（成功判据+时限齐）同样拒
r2 = admit_task({"success_criteria": "x", "time_limit": "1h"})
assert r2["admitted"] is False, "只缺失败判据也应拒启"

# 断言②：三元组齐 → 放行
r3 = admit_task({"success_criteria": "全 PASS", "failure_criteria": "任一非 0 退出码",
                 "time_limit": "18:00"})
assert r3["admitted"] is True, f"三元组齐应放行, got {r3}"
assert not r3["missing"]

print("PASS")
