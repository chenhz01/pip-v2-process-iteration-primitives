# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L74 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

# 断言①: 同资源双写意图（时间窗重叠）报冲突
a = [{"agent": "A", "resource": "src/api.py", "window": (10, 20)},
     {"agent": "B", "resource": "src/api.py", "window": (15, 30)}]
ra = impl.write_gate(a)
assert len(ra["conflicts"]) == 1, "同资源重叠写应报冲突: %r" % ra
assert ra["conflicts"][0]["resource"] == "src/api.py"
assert set(ra["conflicts"][0]["agents"]) == {"A", "B"}
assert ra["clear"] == [], "冲突资源不得进放行清单"

# 断言②: 不同资源放行
b = [{"agent": "A", "resource": "src/api.py", "window": (10, 20)},
     {"agent": "B", "resource": "src/ui.py", "window": (10, 20)}]
rb = impl.write_gate(b)
assert rb["conflicts"] == [], "不同资源不应报冲突"
assert sorted(rb["clear"]) == ["src/api.py", "src/ui.py"], "两资源都应放行"

# 负对照1: 同资源但时间窗不重叠 → 不算冲突
c = [{"agent": "A", "resource": "f.txt", "window": (10, 20)},
     {"agent": "B", "resource": "f.txt", "window": (25, 30)}]
rc = impl.write_gate(c)
assert rc["conflicts"] == [] and rc["clear"] == ["f.txt"], "串行写同一文件应放行"

# 负对照2: 边界相触（A 结束时刻 == B 开始时刻）视为不重叠
d = [{"agent": "A", "resource": "f.txt", "window": (10, 20)},
     {"agent": "B", "resource": "f.txt", "window": (20, 30)}]
assert impl.write_gate(d)["conflicts"] == [], "端点相接不算重叠"

# 负对照3: 非法输入要报错
try:
    impl.write_gate(None)
    raise AssertionError("非列表输入应报 ValueError")
except ValueError:
    pass

print("PASS")
