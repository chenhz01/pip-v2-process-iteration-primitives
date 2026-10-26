# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L101 绝对化红灯：「全部成功、完美无缺、一次通过」一出就先扣分——
说这么满多半是没认真查。命中绝对化词表即封顶评分（cap 0.6），
并要求改写为具体数字。
（词表对齐内部资产 an internal five-gate judge module，原语化入列）
"""

ABSOLUTE_WORDS = ("全部", "全都", "没有任何", "为零", "一次通过", "完美",
                  "100%", "毫无疑问", "绝对")
CAP = 0.6


def absolute_hits(text):
    """命中了哪些绝对化词（按词表顺序，可定位到词）。"""
    if not isinstance(text, str):
        return []
    return [w for w in ABSOLUTE_WORDS if w in text]


def redlight(text, base=1.0, cap=CAP):
    """评分闸：命中绝对化 → 分数封顶 cap，同时给出改写要求。
    返回 {"score": 分, "capped": 是否封顶, "hits": 命中词, "verdict": ...}
    """
    if not isinstance(text, str):
        return {"score": 0.0, "capped": False, "hits": [],
                "verdict": "非文本输入，不给分"}
    hits = absolute_hits(text)
    if hits:
        return {"score": min(base, cap), "capped": True, "hits": hits,
                "verdict": "绝对化命中 %s：分数封顶 %.1f，请改写为具体数字"
                           % ("/".join(hits), cap)}
    return {"score": base, "capped": False, "hits": [],
            "verdict": "无绝对化表述，按实分放行"}


if __name__ == "__main__":
    cases = [
        ("红灯句", "本轮 55 项任务全部成功，完美收官，一次通过。"),
        ("诚实句", "实测 55/55 可跑；坏输入显式契约 32/55，余 23 件靠语言原生报错。"),
        ("混合句", "覆盖率为零的路径已清零。"),
    ]
    for name, t in cases:
        r = redlight(t)
        print("判例[%s] score=%.2f capped=%s —— %s" % (name, r["score"], r["capped"], r["verdict"]))
