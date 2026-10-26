# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L64 幂等键：同一件事不许干两遍。

L1：为每个有副作用的调用生成稳定键（目标+参数哈希），重试时
先查已执行登记——同键二次调用直接回上次结果，不重复执行。
"""

import hashlib
import json


def make_key(target, params):
    """稳定键 = sha256(目标 + 规范化参数) 前 16 位。参数顺序无关。"""
    blob = json.dumps({"t": target, "p": params},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


class IdempotencyRegistry:
    """已执行登记表：key -> 上次结果。execute 返回 (结果, 是否真执行)。"""

    def __init__(self):
        self._store = {}
        self.exec_count = 0

    def execute(self, key, operation, *args, **kwargs):
        """operation 为承载副作用的 callable；同键重试不再执行。"""
        if key in self._store:
            return self._store[key], False
        self.exec_count += 1
        result = operation(*args, **kwargs)
        self._store[key] = result
        return result, True

    def known(self, key):
        return key in self._store


if __name__ == "__main__":
    reg = IdempotencyRegistry()
    calls = []

    def pay(order_id, amount):
        calls.append((order_id, amount))
        return "paid:%s:%s" % (order_id, amount)

    k1 = make_key("pay", {"order": "o1", "amount": 100})
    r1, e1 = reg.execute(k1, pay, "o1", 100)
    r2, e2 = reg.execute(k1, pay, "o1", 100)  # 重试：同参数生成同键
    print("案例1 同键重试 -> 首次执行=%s 二次执行=%s，实际扣款次数=%d"
          % (e1, e2, len(calls)))
    k2 = make_key("pay", {"order": "o2", "amount": 100})
    r3, e3 = reg.execute(k2, pay, "o2", 100)
    print("案例2 不同键   -> 真执行=%s，实际扣款次数=%d" % (e3, len(calls)))
