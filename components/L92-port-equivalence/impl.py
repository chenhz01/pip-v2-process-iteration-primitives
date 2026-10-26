# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L92 移植等价性：把代码搬到新地方，先搬老测试；老测试全过才叫「搬好了」，
不叫「重写了一份像的」。（来源：BeautifulRust——移植必须先搬测试）
"""

DEFAULT_THRESHOLD = 1.0


def check_port_readiness(port):
    """判移植是否达标。port 字段：
      target     —— 目标环境名（必填）
      tests      —— {"migrated": bool, "total": n, "passed": n}
      threshold  —— 通过率达标线，默认 1.0（全过才算搬好）
    返回 (ok, detail)。
    """
    if not isinstance(port, dict) or not (port.get("target") or "").strip():
        return False, {"reason": "缺 target，不知道要搬到哪"}
    t = port.get("tests")
    if not isinstance(t, dict):
        return False, {"reason": "缺 tests 字段：老测试尚未迁移，拦截移植"}
    if not t.get("migrated"):
        return False, {"reason": "测试套件未迁移：不叫移植，叫重写", "tests": t}
    total, passed = t.get("total", 0), t.get("passed", 0)
    if not isinstance(total, int) or not isinstance(passed, int) or total <= 0 or passed < 0:
        return False, {"reason": "total/passed 数字非法", "tests": t}
    if passed > total:
        return False, {"reason": "passed > total，计数有假", "tests": t}
    threshold = port.get("threshold", DEFAULT_THRESHOLD)
    rate = passed / float(total)
    if rate + 1e-9 < threshold:
        return False, {"reason": "通过率 %.2f 低于达标线 %.2f，移植未完成" % (rate, threshold),
                       "pass_rate": rate}
    return True, {"reason": "老测试已迁移且通过率 %.2f 达标，移植完成" % rate, "pass_rate": rate}


if __name__ == "__main__":
    cases = [
        ("未搬测试", {"target": "rust-rewrite", "tests": {"migrated": False}}),
        ("搬了但没过全", {"target": "rust-rewrite",
                          "tests": {"migrated": True, "total": 40, "passed": 37}}),
        ("搬齐过全", {"target": "rust-rewrite",
                      "tests": {"migrated": True, "total": 40, "passed": 40}}),
    ]
    for name, c in cases:
        ok, d = check_port_readiness(c)
        print("判例[%s] ok=%s —— %s" % (name, ok, d["reason"]))
