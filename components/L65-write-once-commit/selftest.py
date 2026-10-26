# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L65 selftest：对齐卡片 L2 两条断言 + 负对照。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from impl import TMP_PREFIX, recover_after_crash, write_once

# 断言①：模拟中断（登记在、临时件在、未提交）后恢复 -> 完成提交
store = {"report.txt": "old"}
intents = {"report.txt": {"status": "WRITTEN_TMP", "content": "new"}}
store[TMP_PREFIX + "report.txt"] = "new"
done, orphans = recover_after_crash(store, intents)
assert done == ["report.txt"], "断言①失败: %r" % done
assert store["report.txt"] == "new", store
assert TMP_PREFIX + "report.txt" not in store and not intents, "登记应销毁"

# 断言②：无登记的孤儿临时文件被识别
store2, intents2 = {}, {}
store2[TMP_PREFIX + "orphan.bin"] = "junk"
done2, orphans2 = recover_after_crash(store2, intents2)
assert orphans2 == ["orphan.bin"], "断言②失败: %r" % orphans2
assert done2 == [], "无登记不得提交: %r" % done2
assert "orphan.bin" not in store2, "孤儿不得转正"

# 负对照1：校验失败 -> 明确失败且不落任何影子状态
store3, intents3 = {}, {}
ok, msg = write_once(store3, intents3, "x.txt", "bad", validate=lambda c: False)
assert ok is False and store3 == {} and intents3 == {}, (ok, msg, store3)

# 负对照2：正常写入后无残留临时件、无残留登记
store4, intents4 = {}, {}
ok2, _ = write_once(store4, intents4, "y.txt", "v1")
assert ok2 is True and TMP_PREFIX + "y.txt" not in store4, store4
assert not intents4, intents4

print("PASS")
