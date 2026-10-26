# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L91 检测件伴随：修好一个 bug，必须同时交「下次怎么提前发现它」的哨兵。

只修不设哨 = 等着它再犯。校验修复产物包含配套检测件（断言/规则/监控项），
缺失则修复不算完成。（来源：php2shell 系列「漏洞+检测规则」成对发布）
"""

ACCEPTED_KINDS = ("assertion", "rule", "monitor")


def check_fix_completeness(fix):
    """判修复是否完成。fix 需含 fixed_target（修了什么）与 detection（检测件）。

    detection 需含 kind（assertion/rule/monitor 之一）与 location（哨兵落点）。
    返回 (ok, reason)；reason 面向人，直接可贴进工单。
    """
    if not isinstance(fix, dict) or not (fix.get("fixed_target") or "").strip():
        return False, "连 fixed_target 都没有，谈不了完整性"
    det = fix.get("detection")
    if not isinstance(det, dict) or not det:
        return False, "只修不设哨：缺配套检测件（断言/规则/监控项），修复不算完成"
    if det.get("kind") not in ACCEPTED_KINDS:
        return False, "检测件 kind 非法（需 assertion/rule/monitor 之一），哨兵立不住"
    if not (det.get("location") or "").strip():
        return False, "检测件缺 location（落在哪、怎么触发），哨兵不可执行"
    return True, "修复+检测件（%s@%s）齐备，修复完成" % (det["kind"], det["location"])


def completeness_rate(fixes):
    """批量体检：返回 (完成数, 未完成清单)。"""
    done, failed = 0, []
    for f in fixes:
        ok, why = check_fix_completeness(f)
        if ok:
            done += 1
        else:
            failed.append((f.get("fixed_target", "?"), why))
    return done, failed


if __name__ == "__main__":
    batch = [
        {"fixed_target": "越界读 off-by-one（L91 缓冲区）"},
        {"fixed_target": "越界读 off-by-one（L91 缓冲区）",
         "detection": {"kind": "rule", "location": "lint/bounds-check.yaml"}},
        {"fixed_target": "越界读（第三份）",
         "detection": {"kind": "guard"}, },
    ]
    done, failed = completeness_rate(batch)
    print("批量体检：%d/%d 件修复真正完成" % (done, len(batch)))
    for t, why in failed:
        print("  未完成：%s —— %s" % (t, why))
    ok, why = check_fix_completeness(
        {"fixed_target": "demo",
         "detection": {"kind": "assertion", "location": "selftest.py:assert_n"}})
    print("单件复判：%s（%s）" % (ok, why))
