# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L62 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import request_deep_dig

# 断言①：超配额 + 无理由 -> 拒
ok1, i1 = request_deep_dig(6, quota=5, reason="")
assert ok1 is False, "断言①失败: %r" % i1
assert i1["approved"] is False and "缺" in i1["why"], i1

# 断言②：超配额 + 有理由 -> 过
ok2, i2 = request_deep_dig(6, quota=5, reason="唯一含资损证据")
assert ok2 is True, "断言②失败: %r" % i2
assert i2["approved"] is True, i2

# 负对照1：配额内不要求理由
ok3, i3 = request_deep_dig(4, quota=5, reason="")
assert ok3 is True, i3

# 负对照2：空白理由（只有空格）视同无理由，必须拒
ok4, i4 = request_deep_dig(9, quota=5, reason="   ")
assert ok4 is False, i4

print("PASS")
