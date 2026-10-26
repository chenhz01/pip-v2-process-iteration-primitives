# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L61 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import cheap_prefilter

RECORDS = ["ok: job done", "error: db timeout", "ok: cached",
           "error: memory leak", "ok: heartbeat"]

# 断言①：可疑集非空时通过，且只放行命中子集
suspects, info = cheap_prefilter(RECORDS)
assert len(suspects) > 0, "断言①失败：可疑集为空 %r" % info
assert len(suspects) < len(RECORDS), "应只放行子集而非全部: %r" % suspects
assert all("error" in s or "timeout" in s or "leak" in s for s in suspects), suspects
assert info["recall_lower_bound_estimate"] > 0, info

# 断言②：规则表为空 -> 显式报「无法分诊」，绝不放行全部
try:
    cheap_prefilter(RECORDS, rules=[])
except ValueError as e:
    assert "无法分诊" in str(e), "报错文案缺少「无法分诊」: %s" % e
else:
    raise AssertionError("断言②失败：空规则表未报错，静默放行了全部")

# 负对照：干净记录集 -> 可疑集为空但流程正常（这是合法输出，不报错）
suspects2, info2 = cheap_prefilter(["ok: a", "ok: b"])
assert suspects2 == [] and info2["flagged"] == 0, info2

print("PASS")
