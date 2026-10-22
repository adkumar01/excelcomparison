"""Keep a text sidecar (<book>.xlsx.txt) next to every tracked workbook.

Usage:
  python tools/sync_sidecars.py [files...]          write/refresh sidecars
  python tools/sync_sidecars.py --check [files...]  exit 1 if any are missing or stale
With no files, all tracked *.xlsx / *.xlsm files are used.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsx2txt import dump  # noqa: E402


def tracked_workbooks():
    out = subprocess.run(
        ["git", "ls-files", "*.xlsx", "*.xlsm"], capture_output=True, text=True, check=True
    ).stdout
    return [line for line in out.splitlines() if line]


def main(argv):
    check = "--check" in argv
    files = [a for a in argv if a != "--check"] or tracked_workbooks()
    bad = []
    for f in files:
        side = f + ".txt"
        text = dump(f)
        current = None
        if os.path.exists(side):
            with open(side, encoding="utf-8", newline="") as fh:
                current = fh.read()
        if current == text:
            continue
        if check:
            bad.append(side)
        else:
            with open(side, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            print(f"updated {side}")
    if bad:
        print("Missing or stale sidecars (run: python tools/sync_sidecars.py):")
        for b in bad:
            print("  " + b)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
