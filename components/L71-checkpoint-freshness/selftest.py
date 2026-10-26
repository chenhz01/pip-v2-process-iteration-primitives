# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L71 selftest — 对齐卡片 L2 两条断言 + 负对照。"""

import impl

DEPS = {"pyyaml": "6.0.1", "requests": "2.31.0"}
FILES = {"main.py": "aaa111", "util.py": "bbb222"}
FP = impl.env_fingerprint(DEPS, FILES)

# 断言①: 指纹不一致拦截（依赖升级）
g = impl.freshness_gate(FP, dict(DEPS, requests="2.32.0"), FILES)
assert g["allow"] is False, "依赖变更应拦截恢复"
assert "拦截" in g["action"], "action 应提示先升级存档"
assert g["stored"] != g["current"], "指纹应不同"

# 断言②: 指纹一致放行
s = impl.freshness_gate(FP, DEPS, FILES)
assert s["allow"] is True and s["action"] == "放行恢复", "环境一致应放行"

# 负对照1: 文件哈希变了也要拦
f = impl.freshness_gate(FP, DEPS, dict(FILES, **{"util.py": "ccc333"}))
assert f["allow"] is False, "文件内容变更应拦截"

# 负对照2: 存档无指纹（空串）不许放行
z = impl.freshness_gate("", DEPS, FILES)
assert z["allow"] is False, "缺指纹的存档不得放行"

# 负对照3: 指纹对键序不敏感（同环境不同插入顺序 → 同指纹）
p2 = impl.env_fingerprint(dict(reversed(list(DEPS.items()))), dict(reversed(list(FILES.items()))))
assert p2 == FP, "指纹应与键序无关"

print("PASS")
