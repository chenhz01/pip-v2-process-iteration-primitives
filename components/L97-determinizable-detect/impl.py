# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L97 可确定化检测：有些活 agent 干了一百遍、每次都一样、从不出错——
这种活就不该再麻烦模型，写成死代码又快又稳。
（来源：HN「每步都该问：这该进代码还是该给模型」）
"""


def determinizable_verdict(history, min_runs=5):
    """对某步骤的历史执行判是否建议确定化。history 为该步骤执行记录列表：
      {"input_sig": 输入模式签名, "output": 输出, "failed": bool}
    判据：最近 min_runs 次——输入模式一致 + 输出恒定 + 零失败 → 建议固化。
    """
    if len(history) < min_runs:
        return {"suggest": False,
                "reason": "历史仅 %d 次（<%d），样本不足以判「每次都一样」" % (len(history), min_runs)}
    recent = history[-min_runs:]
    outputs = [r.get("output") for r in recent]
    failed = [r for r in recent if r.get("failed")]
    sigs = set(r.get("input_sig") for r in recent)
    if failed:
        return {"suggest": False, "reason": "近 %d 次里 %d 次失败：它会出错，固化反而锁死" % (
            min_runs, len(failed))}
    if len(set(outputs)) > 1:
        return {"suggest": False,
                "reason": "近 %d 次输出有 %d 种：输出会变，说明这活需要智能" % (
                    min_runs, len(set(outputs)))}
    return {"suggest": True, "runs": min_runs,
            "reason": "近 %d 次输入模式（%s）一致、输出恒定 %r、零失败 → 建议确定化为死代码" % (
                min_runs, sorted(sigs), outputs[0])}


if __name__ == "__main__":
    const_hist = [{"input_sig": "fixed-A", "output": "OK", "failed": False}
                  for _ in range(100)]
    vary_hist = ([{"input_sig": "fixed-A", "output": "OK", "failed": False}] * 99 +
                 [{"input_sig": "fixed-A", "output": "RETRY-LATER", "failed": False}])
    fail_hist = [{"input_sig": "fixed-A", "output": "OK", "failed": False}] * 9 + \
                [{"input_sig": "fixed-A", "output": "OK", "failed": True}]
    for name, h in (("100 次恒定", const_hist), ("输出有变化", vary_hist),
                    ("有失败", fail_hist), ("样本不足", const_hist[:2])):
        v = determinizable_verdict(h)
        print("判例[%s] suggest=%s —— %s" % (name, v["suggest"], v["reason"]))
