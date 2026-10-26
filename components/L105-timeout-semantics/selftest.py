# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L105 selftest — 对齐卡片 L2 两条断言。"""
import impl

REG = {"http_get": "cancellable", "bank_transfer": "uncancellable"}

# 断言①：不可取消类拦截盲重试（转账超时后必须 BLOCK）
r1 = impl.decide_retry("bank_transfer", REG, retries_done=0)
assert r1["verdict"] == "BLOCK", "不可取消类超时后必须拦截盲重试"
assert r1["semantics"] == "uncancellable", "拦截理由必须指向 uncancellable 语义"

# 断言②：可取消类允许重试（GET 超时后 ALLOW）
r2 = impl.decide_retry("http_get", REG, retries_done=0)
assert r2["verdict"] == "ALLOW", "可取消类超时后应允许重试"

# 负对照：语义未登记的工具也必须拦（分不清 = 不许赌）
r3 = impl.decide_retry("unknown_tool", REG)
assert r3["verdict"] == "BLOCK" and r3["semantics"] == "unknown", "语义未登记必须拦截"

# 补充：可取消类到达上限同样 BLOCK
r4 = impl.decide_retry("http_get", REG, retries_done=3, max_retries=3)
assert r4["verdict"] == "BLOCK", "可取消类超上限也应拦截"

print("PASS L105: 不可取消拦截(断言①) / 可取消放行(断言②) / 未登记负对照 / 上限拦截 共4断言全过")
