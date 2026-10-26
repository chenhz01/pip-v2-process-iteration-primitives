# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L101 selftest：断言对齐卡片 L2（①「全部成功」触发封顶 ②「55/55 可跑」不触发）。"""

import sys

from impl import ABSOLUTE_WORDS, CAP, absolute_hits, redlight


def main():
    # 词表与内部资产 an internal five-gate judge module 逐词对齐
    assert ABSOLUTE_WORDS == ("全部", "全都", "没有任何", "为零", "一次通过",
                              "完美", "100%", "毫无疑问", "绝对"), "词表必须逐词对齐内部资产"

    # L2-1 「全部成功」触发封顶
    r1 = redlight("本轮 55 项任务全部成功，毫无疑问。")
    assert r1["capped"], "L2-1 失败：「全部成功」应触发封顶"
    assert r1["score"] == CAP and "全部" in r1["hits"] and "毫无疑问" in r1["hits"]
    assert "具体数字" in r1["verdict"], "应要求改写为具体数字"

    # L2-2 「55/55 可跑」不触发
    r2 = redlight("实测 55/55 可跑；坏输入显式契约 32/55。")
    assert not r2["capped"], "L2-2 失败：具体数字表述不应触发封顶"
    assert r2["score"] == 1.0 and r2["hits"] == []

    # 负对照：每个词表词都要能触发（尺子对词表全覆盖）
    for w in ABSOLUTE_WORDS:
        r = redlight("长度足以通过审查的句子，其中出现了「%s」这个词。" % w)
        assert r["capped"], "词「%s」必须触发封顶" % w
        assert w in r["hits"]
    # 非文本输入不给分
    r3 = redlight(None)
    assert r3["score"] == 0.0 and not r3["capped"]

    print("PASS: L101 绝对化红灯，词表对齐+L2 两条全覆盖+9 词逐一负对照，全过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
