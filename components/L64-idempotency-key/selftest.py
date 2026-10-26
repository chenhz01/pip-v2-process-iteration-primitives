# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L64 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import IdempotencyRegistry, make_key

calls = []


def pay(order_id, amount):
    calls.append((order_id, amount))
    return "paid:%s:%s" % (order_id, amount)


# 断言①：同键二次调用不重复执行
reg = IdempotencyRegistry()
k1 = make_key("pay", {"order": "o1", "amount": 100})
k1_retry = make_key("pay", {"amount": 100, "order": "o1"})  # 参数顺序无关
assert k1 == k1_retry, "键必须对参数顺序稳定: %s vs %s" % (k1, k1_retry)
r1, e1 = reg.execute(k1, pay, "o1", 100)
r2, e2 = reg.execute(k1_retry, pay, "o1", 100)
assert e1 is True and e2 is False, "断言①失败: 执行标记 %r/%r" % (e1, e2)
assert r1 == r2 and len(calls) == 1, "同键重试不得重复执行: %r" % calls
assert reg.exec_count == 1, reg.exec_count

# 断言②：不同键正常执行
k2 = make_key("pay", {"order": "o2", "amount": 100})
r3, e3 = reg.execute(k2, pay, "o2", 100)
assert e3 is True and len(calls) == 2, "断言②失败: %r" % calls

# 负对照：参数不同 -> 键必不同，不许误判为重复
k3 = make_key("pay", {"order": "o1", "amount": 200})
assert k3 != k1, "不同参数不得撞键"
_, e4 = reg.execute(k3, pay, "o1", 200)
assert e4 is True and len(calls) == 3, calls

print("PASS")
