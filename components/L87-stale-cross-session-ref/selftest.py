# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L87 selftest v1.1：对齐卡片 L2 ①失效报警 ②有效不报 + 日跑实测抓到的假阳性负对照。"""
import os

from impl import scan_refs

exists = os.path.exists
here = os.path.dirname(os.path.abspath(__file__))

# 断言①：确证的失效本地路径 → 报警并列清单
bad_text = "配置在 /no/such/file-xyz.cfg，日志在 /tmp/gone-forever.log"
r1 = scan_refs(bad_text, exists=exists)
assert r1["alarm"] is True, f"失效路径应报警, got {r1}"
assert "/no/such/file-xyz.cfg" in r1["broken"] or "/tmp/gone-forever.log" in r1["broken"], r1

# 断言②：引用全部有效 → 不报
good_path = os.path.join(here, "impl.py")
r2 = scan_refs(f"文件在 {good_path}", exists=exists)
assert r2["alarm"] is False, f"有效引用不应报, got {r2}"

# 负对照①（日跑实测假阳性）：行内记法不是路径，绝不能报警
r3 = scan_refs("写法如 /影响面/历史失败率、/balanced/max、/规则/小模型", exists=exists)
assert r3["alarm"] is False, f"行内记法被误判成路径: {r3['broken']}"

# 负对照②：离线验不了的 URL 默认不判失效，单列 unverified_urls（不说假话）
r4 = scan_refs("参考 https://ghost.example/gone 与 https://ok.example/doc", exists=exists)
assert r4["alarm"] is False, "URL 离线不可验证，默认不得判失效"
assert "https://ghost.example/gone" in r4["unverified_urls"], r4

# strict 模式：URL 未知也当失效（留给确有网络的调用方）
r5 = scan_refs("参考 https://ghost.example/gone", strict=True, exists=exists)
assert r5["alarm"] is True and "https://ghost.example/gone" in r5["broken"], r5

print("PASS 5/5 assertions (含 2 条假阳性负对照)")
