# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L82 缓存感知剪枝 — 删上下文不是免费的：删中间一段，后面全部要重算。

L1: 输入剪枝方案（位置/长度），估算缓存重算成本 vs token 节省；
    负收益 → 否决，并建议改尾部删。
"""
SAVE_PER_TOKEN = 1.0       # 删 1 个 token 的节省（窗口/计费维度）
RECOMPUTE_PER_TOKEN = 2.0  # 前缀缓存失效后重算 1 个 token 的代价


def evaluate(segments, index) -> dict:
    """segments: [{"id","tokens"}] 按序排列；提案：删除 segments[index]。
    位于其后的全部 token 失去前缀缓存需重算；净收益 = 节省 - 重算。"""
    pruned = segments[index]["tokens"]
    after = sum(s["tokens"] for s in segments[index + 1:])
    saving = pruned * SAVE_PER_TOKEN
    recompute = after * RECOMPUTE_PER_TOKEN
    net = saving - recompute
    out = {"verdict": "VETO" if net < 0 else "APPROVE", "pruned_tokens": pruned,
           "tokens_after": after, "saving": saving, "recompute": recompute,
           "net": round(net, 1), "suggestion": None}
    if out["verdict"] == "VETO":
        out["suggestion"] = f"改尾部删（净收益 +{saving:.0f}）或分批删最小必要段"
    return out


if __name__ == "__main__":
    segs = [{"id": f"s{i}", "tokens": t} for i, t in enumerate([200, 100, 200, 200, 200])]
    r1 = evaluate(segs, 1)
    print(f"[中部删 100tok/其后 600tok] 判定={r1['verdict']} "
          f"净收益={r1['net']}(省{r1['saving']} vs 赔{r1['recompute']}) 建议={r1['suggestion']}")
    r2 = evaluate(segs, 4)
    print(f"[尾部删 200tok/其后 0tok] 判定={r2['verdict']} 净收益=+{r2['net']}")
