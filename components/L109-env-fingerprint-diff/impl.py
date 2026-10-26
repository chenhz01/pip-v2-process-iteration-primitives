# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L109 环境指纹对比 — 恢复现场前先核对"这是不是当初那个房间"。

L1：恢复/复用前采集环境指纹（平台/Python 版本/依赖哈希/工作目录前缀）
    与存档指纹比对：不一致 → 要求确认或重建；一致 → 直接恢复；
    当前环境缺指纹项 → 无法判定，要求重建（缺项比不一致更危险）。
"""


def compare_env(archived_fp, current_fp):
    """逐项比对环境指纹字典；缺项/不一致/一致 三档裁决。"""
    missing = sorted(set(archived_fp) - set(current_fp))
    extra = sorted(set(current_fp) - set(archived_fp))
    if missing:
        return {"verdict": "REBUILD", "missing": missing, "mismatched": [], "extra": extra,
                "reason": "当前环境缺指纹项 %s：无法判定是不是同一个房间，要求重建" % missing}
    mismatched = sorted(k for k in archived_fp if archived_fp[k] != current_fp[k])
    if mismatched or extra:
        return {"verdict": "CONFIRM", "missing": [], "mismatched": mismatched, "extra": extra,
                "reason": "指纹不符：%s；恢复前要求人工确认或重建"
                          % ", ".join("%s: %r != %r" % (k, archived_fp[k], current_fp[k])
                                      for k in mismatched)}
    return {"verdict": "RESUME", "missing": [], "mismatched": [], "extra": [],
            "reason": "指纹逐项一致，直接恢复"}


if __name__ == "__main__":
    saved = {"platform": "win32", "python": "3.13.12", "workdir": "C:/proj",
             "deps_hash": "a1b2c3"}
    same = dict(saved)
    moved = dict(saved, workdir="D:/elsewhere")
    upgraded = dict(saved, python="3.14.0")
    partial = {"platform": "win32", "python": "3.13.12"}
    for tag, cur in [("完全一致", same), ("工作目录变了", moved),
                     ("Python 升级", upgraded), ("缺 deps_hash", partial)]:
        r = compare_env(saved, cur)
        print("[%-8s] -> %-7s | %s" % (tag, r["verdict"], r["reason"]))
