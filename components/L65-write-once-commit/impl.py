# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""L65 恰好一次写：要么写成功一次，要么明确失败，绝不写一半没人管。

L1：写前登记意图 -> 写入临时区 -> 校验 -> 原子提交 -> 销毁登记；
中断恢复时按登记补完提交，并识别无登记的孤儿临时文件。
TMP_PREFIX 模拟"临时区"，store[path] 赋值模拟原子 rename。
"""

TMP_PREFIX = "~tmp:"


def write_once(store, intents, path, content, validate=None):
    """五步写入。validate(content) 为假则回退并明确失败。"""
    intents[path] = {"status": "INTENT", "content": content}
    store[TMP_PREFIX + path] = content
    intents[path]["status"] = "WRITTEN_TMP"
    if validate is not None and not validate(content):
        del store[TMP_PREFIX + path]
        del intents[path]
        return False, "校验失败，已回退，未提交"
    store[path] = content
    del store[TMP_PREFIX + path]
    del intents[path]
    return True, "committed"


def recover_after_crash(store, intents):
    """中断恢复：有登记且临时件在 -> 补完提交；无登记临时件 -> 孤儿。"""
    completed, orphans = [], []
    for path in list(intents):
        tmp = TMP_PREFIX + path
        if tmp in store:
            store[path] = store[tmp]
            del store[tmp]
            completed.append(path)
        del intents[path]
    for key in list(store):
        if key.startswith(TMP_PREFIX) and key[len(TMP_PREFIX):] not in intents:
            orphans.append(key[len(TMP_PREFIX):])
    return completed, orphans


if __name__ == "__main__":
    store, intents = {}, {}
    print("案例1 正常五步写入:",
          write_once(store, intents, "cfg.txt", "v1")[1])
    # 模拟在"临时区写完、还没提交"时崩溃
    store2, intents2 = {}, {}
    intents2["data.bin"] = {"status": "WRITTEN_TMP", "content": "half"}
    store2[TMP_PREFIX + "data.bin"] = "half"
    done, orphan = recover_after_crash(store2, intents2)
    print("案例2 崩溃恢复 -> 补完提交:", done, "终值:", store2.get("data.bin"))
    store2[TMP_PREFIX + "ghost.tmp"] = "??"
    done2, orphan2 = recover_after_crash(store2, intents2)
    print("案例3 孤儿临时文件 ->", orphan2)
