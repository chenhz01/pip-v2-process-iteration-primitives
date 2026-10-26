# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L102 自检：负对照强制的两条 L2 断言 + 负对照（尺子自己先过负对照）。"""
import sys
from impl import run

# 断言①：无负对照的判据必须降级 UNQUALIFIED
r1 = run([{"criterion": "所有输出必须非空"}])
assert r1["rows"][0]["verdict"] == "UNQUALIFIED", "断言①失败：无负对照未降级"

# 断言②：负对照存在且 blocked=True 的判据必须 QUALIFIED
r2 = run([{"criterion": "A",
           "negative_control": {"case": "坏例", "blocked": True}}])
assert r2["rows"][0]["verdict"] == "QUALIFIED", "断言②失败：合格判据被误杀"

# 断言③（负对照）：负对照存在但没拦住（blocked=False）也必须降级
r3 = run([{"criterion": "B",
           "negative_control": {"case": "坏例但放行了", "blocked": False}}])
assert r3["rows"][0]["verdict"] == "UNQUALIFIED", "断言③失败：没拦住的负对照被放行"

# 断言④（整体闸）：判据集未全合格时 verdict 必须是 CRITERIA-NOT-READY
assert r3["verdict"] == "CRITERIA-NOT-READY", "断言④失败：整体闸未触发"

print("PASS L102 4/4 assertions (含 1 条负对照)")
sys.exit(0)
