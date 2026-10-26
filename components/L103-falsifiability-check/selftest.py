# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L103 自检：可证伪化的两条 L2 断言 + 负对照。"""
import sys
from impl import run

# 断言①：无可伪条件必须降级 HYPOTHESIS
r1 = run([{"claim": "本轮日跑比上轮更快"}])
assert r1["rows"][0]["verdict"] == "HYPOTHESIS", "断言①失败：无可伪条件未降级"

# 断言②：附可伪条件保留 CONCLUSION
r2 = run([{"claim": "55 件全部可独立运行", "falsifier": "任一件 selftest 非 0"}])
assert r2["rows"][0]["verdict"] == "CONCLUSION", "断言②失败：合格结论被降级"

# 负对照：空结论文本必须 INVALID（不是平凡放行）
r3 = run([{"claim": ""}])
assert r3["rows"][0]["verdict"] == "INVALID", "负对照失败：空结论未被拦"

print("PASS L103 3/3 assertions (含 1 条负对照)")
sys.exit(0)
