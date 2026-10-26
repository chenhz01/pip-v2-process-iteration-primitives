# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L95 selftest：断言对齐卡片 L2（①余量不足拒开 ②充足放行）。"""

import sys

from impl import ALLOW, DENY, DOWNGRADE, quota_gate


def main():
    # L2-1 余量不足 → 拒开
    v1, d1 = quota_gate(450.0, 500.0, 80.0)
    assert v1 == DENY, "L2-1 失败：余量 50 < 需 80 应拒开"
    assert d1["remaining"] == 50.0

    # L2-2 充足 → 放行
    v2, d2 = quota_gate(120.0, 500.0, 80.0)
    assert v2 == ALLOW, "L2-2 失败：余量 380 > 需 80 应放行"

    # 负对照：烧穿 / 非法日志 / 负数都要拦；夹缝降档可见
    v3, _ = quota_gate(520.0, 500.0, 10.0)
    assert v3 == DENY, "已烧穿应拒"
    v4, _ = quota_gate(float("nan"), 500.0, 10.0)
    assert v4 == DENY, "NaN 用量应拦"
    v5, _ = quota_gate(-1, 500.0, 10.0)
    assert v5 == DENY, "负数用量应拦"
    v6, _ = quota_gate(120.0, 500.0, 380.0, 20.0)
    assert v6 == DOWNGRADE, "余量只够裸任务、装不下安全垫应降档"

    print("PASS: L95 配额余量闸，6 条断言全过（L2 两条全覆盖+4 负对照）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
