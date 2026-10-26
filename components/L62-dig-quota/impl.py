# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L62 深挖配额：仔细看一份记录很贵，一天只许深挖固定几份。

L1：记录深挖次数与预算；超配额必须附「为什么这份值得」字段，
缺字段拒绝。
"""


def request_deep_dig(dug_today, quota=5, reason=""):
    """dug_today: 今天已深挖次数；quota: 配额；reason: 理由字段。

    返回 (approved, info)。配额内直接过；超配额时 reason 缺失 -> 拒。
    """
    used = int(dug_today)
    if used < quota:
        return True, {"approved": True, "used": used, "quota": quota,
                      "why": "配额内（%d/%d），直接放行" % (used, quota)}
    if not str(reason).strip():
        return False, {"approved": False, "used": used, "quota": quota,
                       "why": "已超配额（%d/%d）且缺「为什么这份值得」"
                              "字段，拒绝" % (used, quota)}
    return True, {"approved": True, "used": used, "quota": quota,
                  "why": "超配额（%d/%d）但附有效理由：%s"
                         % (used, quota, reason)}


if __name__ == "__main__":
    a1, i1 = request_deep_dig(2, quota=5)
    print("案例1 第3次深挖（配额5）  ->", "通过" if i1["approved"] else "拒绝",
          "理由:", i1["why"])
    a2, i2 = request_deep_dig(6, quota=5, reason="")
    print("案例2 第7次、无理由       ->", "通过" if i2["approved"] else "拒绝",
          "理由:", i2["why"])
    a3, i3 = request_deep_dig(6, quota=5, reason="唯一一份含资损证据的记录")
    print("案例3 第7次、有理由       ->", "通过" if i3["approved"] else "拒绝",
          "理由:", i3["why"])
