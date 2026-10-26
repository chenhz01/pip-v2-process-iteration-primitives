# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L93 selftest：断言对齐卡片 L2（①分歧点被定位 ②一致判 PASS）。"""

import sys

from impl import cross_impl_check, slugify_v1, slugify_v2, slugify_v3


def main():
    fixed = ["Hello World", "  padded  ", "A B C"]

    # L2-1 分歧点被定位
    r1 = cross_impl_check(fixed, slugify_v1, slugify_v2)
    assert not r1["equivalent"], "L2-1 失败：有分歧应判不等价"
    assert r1["divergence_index"] == 1, "首个分歧应定位在下标 1"
    assert r1["out_a"] == "padded" and r1["out_b"] == "--padded--", "应给出两侧输出供定位"
    # 负对照：空输入集不算验证通过
    r0 = cross_impl_check([], slugify_v1, slugify_v2)
    assert not r0["equivalent"], "空输入集不应判等价"

    # L2-2 一致判 PASS
    r2 = cross_impl_check(fixed, slugify_v1, slugify_v3)
    assert r2["equivalent"], "L2-2 失败：独立重写且语义一致应判 PASS"
    assert r2["checked"] == 3 and r2["divergence_index"] is None

    print("PASS: L93 跨实现等价，4 条断言全过（L2 两条全覆盖+1 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
