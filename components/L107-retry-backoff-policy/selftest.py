# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L107 selftest — 对齐卡片 L2 两条断言。"""
import impl

# 断言①：零间隔连击拦截（[0,0,0] 必须 VIOLATED 且逐条指出）
r1 = impl.check_backoff([0, 0, 0])
assert r1["verdict"] == "VIOLATED", "零间隔连击必须拦截"
assert len(r1["violations"]) == 3, "三次零间隔应各报一条违规"

# 断言②：合规退避放行（1/2/4/8 指数序列 → COMPLIANT）
r2 = impl.check_backoff([1.0, 2.0, 4.0, 8.0])
assert r2["verdict"] == "COMPLIANT" and r2["violations"] == [], "合规指数退避应放行"

# 负对照①：越等越短（反向退避）必须拦
r3 = impl.check_backoff([8.0, 4.0, 2.0])
assert r3["verdict"] == "VIOLATED", "反向退避必须拦截"
assert any("指数退避" in v for v in r3["violations"]), "应指出未达指数退避"

# 负对照②：总次数超封顶必须拦
r4 = impl.check_backoff([1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0], max_retries=6)
assert r4["verdict"] == "VIOLATED" and any("超封顶" in v for v in r4["violations"]), \
    "总次数超封顶必须拦截"

print("PASS L107: 零间隔连击拦截(断言①) / 合规退避放行(断言②) / 反向退避+超封顶负对照 共4断言全过")
