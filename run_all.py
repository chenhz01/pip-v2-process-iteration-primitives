# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01
"""Run every component in this repo: selftest.py and impl.py, each in its own process."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(ROOT, "components")
PY = sys.executable


def main():
    dirs = sorted(d for d in os.listdir(COMP) if os.path.isdir(os.path.join(COMP, d)))
    ok_n = 0
    for d in dirs:
        base = os.path.join(COMP, d)
        row = {}
        for name, key in (("selftest.py", "selftest_ok"), ("impl.py", "demo_ok")):
            p = os.path.join(base, name)
            if not os.path.exists(p):
                row[key] = False; row[key + "_err"] = "missing " + name; continue
            r = subprocess.run([PY, p], cwd=base, capture_output=True, text=True,
                               timeout=120, encoding="utf-8", errors="replace")
            row[key] = r.returncode == 0
            if r.returncode != 0:
                row[key + "_err"] = (r.stderr or "")[-400:]
        good = row.get("selftest_ok") and row.get("demo_ok")
        ok_n += 1 if good else 0
        print("%-42s selftest=%-5s demo=%-5s %s" % (
            d, row.get("selftest_ok"), row.get("demo_ok"),
            "" if good else "<< " + str(row.get("selftest_err") or row.get("demo_err"))[:110]))
    print("\n== %d/%d components green ==" % (ok_n, len(dirs)))
    return 0 if ok_n == len(dirs) else 1


if __name__ == "__main__":
    sys.exit(main())
