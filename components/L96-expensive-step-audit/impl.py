# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L96 昂贵步骤前置审计：花大钱的那一步之前必须有一次「过堂」——
这一步真的必要吗？有没有更省的走法？缺审计不放行。
"""


def audit_expensive_step(step):
    """step 字段：
      name       —— 步骤名
      expensive  —— 是否标记为昂贵
      audit      —— {"necessity": 必要性, "alternative": 替代方案}（昂贵时必填）
    返回 (ok, reason)。
    """
    if not isinstance(step, dict) or not (step.get("name") or "").strip():
        return False, "缺 name，不知道过的是哪堂"
    if not step.get("expensive"):
        return True, "「%s」未标记昂贵，无需过堂" % step["name"]
    a = step.get("audit")
    if not isinstance(a, dict) or not a:
        return False, "昂贵步骤「%s」无审计记录：花大钱前必须过堂" % step["name"]
    missing = [f for f in ("necessity", "alternative") if not (a.get(f) or "").strip()]
    if missing:
        return False, "昂贵步骤「%s」审计缺字段 %s：说不出替代方案就先别花钱" % (
            step["name"], "/".join(missing))
    return True, "「%s」过堂齐备（必要性+替代方案），放行" % step["name"]


def scan_plan(steps):
    """扫整个计划，昂贵步骤没过堂的列出来。返回 (通过数, 拦截清单)。"""
    ok_n, blocked = 0, []
    for s in steps:
        good, why = audit_expensive_step(s)
        if good:
            ok_n += 1
        else:
            blocked.append((s.get("name", "?"), why))
    return ok_n, blocked


if __name__ == "__main__":
    plan = [
        {"name": "grep 日志", "expensive": False},
        {"name": "全量回归测试", "expensive": True,
         "audit": {"necessity": "发布前唯一可信验证", "alternative": "抽样 200 例已先跑过"}},
        {"name": "全量重建索引", "expensive": True,
         "audit": {"necessity": "must"}},
    ]
    ok_n, blocked = scan_plan(plan)
    print("计划体检：%d/%d 步放行" % (ok_n, len(plan)))
    for n, why in blocked:
        print("  拦截：%s —— %s" % (n, why))
