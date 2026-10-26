# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L110 对外敏感面扫描 — 拿出去给人看之前，最后扫一遍。

L1：对待发布产物扫描敏感词表（凭据样串/API 密钥/内部路径/内部规则名），
    命中即拦并列出行号与类别；干净产物放行。
"""
import re

PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "API 密钥样串"),
    (r"AKIA[0-9A-Z]{16}", "云平台 AccessKey"),
    (r"(?i)\b(password|secret|token|api_key)\s*[:=]\s*['\"]?[^\s'\"]{6,}", "凭据赋值"),
    (r"[A-Za-z]:\\+Users\\+[A-Za-z0-9_]+", "Windows 用户路径"),
    (r"/home/[a-z0-9_]+", "Linux 家目录路径"),
    (r"(?i)(internal[-_ ]?use[-_ ]?only|do not distribute)", "内部资产标记"),
]


def scan_sensitive(text):
    """逐行扫描，命中返回 (行号, 类别, 脱敏样例)。verdict: BLOCK/CLEAN。"""
    hits = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pat, kind in PATTERNS:
            m = re.search(pat, line)
            if m:
                s = m.group(0)
                masked = s[:4] + "***" + s[-2:] if len(s) > 8 else s[:2] + "***"
                hits.append({"line": lineno, "kind": kind, "sample": masked})
    return {"verdict": "BLOCK" if hits else "CLEAN", "hits": hits}


if __name__ == "__main__":
    dirty = ("# 发布说明 v2\n"
             "密钥配置: api_key = 'sk-abcdef1234567890abcdef1234'\n"
             "日志存于 C:\\Users\\chenhz01\\logs\\run.txt\n")
    clean = ("# 发布说明 v2\n"
             "本次共 7 件原语，selftest 全部 PASS。\n"
             "认证请使用环境变量注入，不要硬编码。\n")
    r1, r2 = scan_sensitive(dirty), scan_sensitive(clean)
    print("[1] 脏产物判定: %s | 命中 %d 处" % (r1["verdict"], len(r1["hits"])))
    for h in r1["hits"]:
        print("    第%d行 [%s] 样例: %s" % (h["line"], h["kind"], h["sample"]))
    print("[2] 干净产物判定: %s | 命中 %d 处" % (r2["verdict"], len(r2["hits"])))
