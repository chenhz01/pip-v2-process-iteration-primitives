# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L87 跨会话陈旧引用：新会话开场时扫描历史引用并验存在性，失效列清单。

v1.1 修订（日跑实测反馈，双环闭环）：
  - 路径正则限定 ASCII 段 + 文件必须有扩展名——消灭 `/影响面/历史失败率`、
    `/balanced/max` 这类行内记法的假阳性（16 处全是它）。
  - URL 离线不可验证：默认不判「失效」，单列 unverified_urls；strict=True 才报警。
    不把「没法验」说成「已失效」——那是假话。
"""

import os
import re

URL_RE = re.compile(r"https?://[^\s，。、\)\"'`]+", re.IGNORECASE)
# 相对路径：段内仅 ASCII 文件名字符，且末段必须带扩展名（r23/daily_run_2026-10-24.json）
REL_RE = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+\.[A-Za-z0-9_\-]{1,12}")
# 绝对路径：/tmp/gone-forever.log（同样 ASCII + 末段带扩展名）
ABS_RE = re.compile(r"/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*\.[A-Za-z0-9_\-]{1,12}")
# Windows 盘符路径：C:\Users\...
WIN_RE = re.compile(r"[A-Za-z]:[/\\][\w .\-/\\]+")


def scan_refs(text, valid_urls=(), exists=os.path.exists, strict=False):
    """扫描文本中的引用，逐一验证存在性。

    返回 {"broken": [...本地失效路径], "unverified_urls": [...离线验不了的 URL],
          "alarm": bool}。alarm 只由「确证的失效路径」（及 strict 下的 URL）触发。
    """
    broken, unverified = [], []
    rest = text
    for url in URL_RE.findall(text):
        rest = rest.replace(url, " ")
        if url in valid_urls:
            continue
        if strict:
            broken.append(url)
        else:
            unverified.append(url)
    seen = set()
    for pat in (WIN_RE, REL_RE, ABS_RE):
        for path in pat.findall(rest):
            p = path.strip().strip("，。、")
            if p in seen:
                continue
            seen.add(p)
            if not exists(p):
                broken.append(p)
    return {"broken": broken, "unverified_urls": unverified, "alarm": bool(broken)}


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    self_path = os.path.join(here, "impl.py")  # 真实存在的文件
    text = ("上次说的配置在 %s，行内记法 /影响面/历史失败率 与 /balanced/max 不是路径，"
            "文档见 https://example.invalid/old-doc，日志在 /tmp/gone-forever.log" % self_path)
    r = scan_refs(text, valid_urls=set())
    print("[demo] 判了什么: 报警=%s | 失效路径=%s | 离线未验 URL=%d 个"
          % (r["alarm"], r["broken"], len(r["unverified_urls"])))
