"""Regenerate the full report pack (reports 11-40). Run from repo root:
    .venv/bin/python reports/generators/build_all.py
Each module is deterministic and idempotent; charts land in reports/charts/,
PDFs in reports/. Reports 01-10 are the original pack (not regenerated here).
"""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = ["corporate", "strategy", "brands", "brands2", "functional", "insights", "customers"]

def main():
    built = []
    for name in MODULES:
        mod = importlib.import_module(name)
        for fn in sorted(dir(mod)):
            if fn.startswith("r") and fn[1:3].isdigit() and callable(getattr(mod, fn)):
                path = getattr(mod, fn)()
                built.append(os.path.basename(path))
                print("built", os.path.basename(path))
    print(f"\n{len(built)} reports built.")
    return built

if __name__ == "__main__":
    main()
