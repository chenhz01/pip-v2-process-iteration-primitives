# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L110 selftest — 对齐卡片 L2 两条断言。"""
import impl

# 断言①：含密钥样串拦截（sk-... 必须命中并给出行号+类别）
DIRTY = "说明：\napi_key = 'sk-abcdef1234567890abcdef1234'\n完\n"
r1 = impl.scan_sensitive(DIRTY)
assert r1["verdict"] == "BLOCK", "含密钥样串必须拦截"
assert any(h["kind"] == "API 密钥样串" for h in r1["hits"]), "必须识别为 API 密钥类别"
assert any(h["line"] == 2 for h in r1["hits"]), "必须给出命中行号"
assert all("***" in h["sample"] for h in r1["hits"]), "样例必须脱敏，不得原样外泄"

# 断言②：干净产物放行（零命中 → CLEAN）
CLEAN = "说明：\n7 件原语 selftest 全 PASS，认证走环境变量。\n"
r2 = impl.scan_sensitive(CLEAN)
assert r2["verdict"] == "CLEAN" and r2["hits"] == [], "干净产物应放行"

# 负对照①：内部路径（Windows 用户路径）也必须拦
r3 = impl.scan_sensitive("日志在 C:\\Users\\chenhz01\\logs\\a.txt")
assert r3["verdict"] == "BLOCK" and any(h["kind"] == "Windows 用户路径" for h in r3["hits"]), \
    "内部路径必须拦截"

# 负对照②：内部资产标记必须拦（对外版用通用标记串，不再自指本项目代号）
r4 = impl.scan_sensitive("header: INTERNAL USE ONLY — do not distribute")
assert r4["verdict"] == "BLOCK" and any(h["kind"] == "内部资产标记" for h in r4["hits"]), \
    "内部资产标记必须拦截"

print("PASS L110: 密钥样串拦截(断言①) / 干净放行(断言②) / 内部路径+内部标记负对照 共4断言全过")
