# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L93 跨实现等价：同一功能有两份实现时，同样输入必须喂出同样答案；
不一致就说明有一份是错的。固定输入集跑双实现，diff 并定位首个分歧点。
"""


def cross_impl_check(inputs, impl_a, impl_b):
    """对固定输入集逐个喂双实现，返回等价报告：
      equivalent        —— 全部一致才 True
      divergence_index  —— 首个分歧输入的下标（一致时 None）
      out_a / out_b     —— 分歧点两侧的输出（定位用）
    """
    if not inputs:
        return {"equivalent": False, "reason": "输入集为空，等于什么都没验"}
    for i, x in enumerate(inputs):
        a, b = impl_a(x), impl_b(x)
        if a != b:
            return {"equivalent": False, "divergence_index": i,
                    "input": x, "out_a": a, "out_b": b,
                    "reason": "第 %d 个输入即分歧：同一份功能不该有两套答案" % i}
    return {"equivalent": True, "checked": len(inputs), "divergence_index": None,
            "reason": "双实现 %d 个输入全部一致，判 PASS" % len(inputs)}


def slugify_v1(s):
    """参考实现：小写+空格转连字符。"""
    return s.strip().lower().replace(" ", "-")


def slugify_v2(s):
    """第二实现：抄 v1 时把 strip 抄丢了——低 ascii 前后空白会露馅。"""
    return s.lower().replace(" ", "-")


def slugify_v3(s):
    """第三实现：独立重写，与 v1 语义一致。"""
    out = []
    for ch in s.strip().lower():
        out.append("-" if ch == " " else ch)
    return "".join(out)


if __name__ == "__main__":
    fixed_inputs = ["Hello World", "  padded  ", "A B C", "x"]
    r1 = cross_impl_check(fixed_inputs, slugify_v1, slugify_v2)
    print("对 v1 vs v2：equivalent=%s" % r1["equivalent"])
    print("  判语：%s" % r1["reason"])
    if r1.get("divergence_index") is not None:
        print("  首个分歧点：输入 %r → v1=%r, v2=%r"
              % (r1["input"], r1["out_a"], r1["out_b"]))
    r2 = cross_impl_check(fixed_inputs, slugify_v1, slugify_v3)
    print("对 v1 vs v3：equivalent=%s（%s）" % (r2["equivalent"], r2["reason"]))
