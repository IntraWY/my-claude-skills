#!/usr/bin/env python
"""Verify whether local GAS source matches what is LIVE on Apps Script.

`clasp status` only lists files that would be pushed; it does NOT compare to the
deployed script. This pulls the live source into a temp dir and byte-diffs it
against the local files, handling Thai folder names (Python cwd= + clasp.cmd).

Usage:
    python verify_live.py <dir1> [<dir2> ...]
    # dirs are sub-project folder names relative to repo root, e.g. RPA_B2_TO_C1 เบิกของ

Output per file: SAME / DIFF with byte sizes.
  local size > LIVE size  -> local newer, NOT deployed yet
  LIVE size  > local size -> local stale, pull first
  same size + DIFF        -> usually just CRLF (clasp pull returns LF)
"""
import subprocess, os, sys, tempfile, shutil, filecmp, json

sys.stdout.reconfigure(encoding="utf-8")

FILES = ["code.js", "Index.html", "appsscript.json"]
ROOT = os.getcwd()
BASE = os.path.join(tempfile.gettempdir(), "clasp-verify")


def find_repo_root(start):
    d = start
    while True:
        if os.path.exists(os.path.join(d, "deploy-config.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return start
        d = parent


def verify(folder):
    src = os.path.join(ROOT, folder)
    cfg_path = os.path.join(src, ".clasp.json")
    if not os.path.exists(cfg_path):
        print(f"=== {folder} === SKIP (no .clasp.json)")
        return
    with open(cfg_path, encoding="utf-8") as f:
        sid = json.load(f).get("scriptId")
    tmp = os.path.join(BASE, folder)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    with open(os.path.join(tmp, ".clasp.json"), "w", encoding="utf-8") as f:
        json.dump({"scriptId": sid, "rootDir": tmp}, f)
    print(f"=== {folder} (scriptId {sid[:12]}...) ===")
    r = subprocess.run(["clasp.cmd", "pull"], cwd=tmp, capture_output=True,
                       text=True, timeout=90, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("  PULL ERR:", (r.stderr or r.stdout).strip()[:200])
        return
    for fn in FILES:
        a, b = os.path.join(src, fn), os.path.join(tmp, fn)
        if not os.path.exists(b):
            print(f"  {fn}: LIVE=missing")
            continue
        if not os.path.exists(a):
            print(f"  {fn}: local=missing")
            continue
        same = filecmp.cmp(a, b, shallow=False)
        sa, sb = os.path.getsize(a), os.path.getsize(b)
        hint = ""
        if not same:
            hint = "  <- local NEWER (not deployed)" if sa > sb else \
                   "  <- local STALE (pull first)" if sb > sa else \
                   "  <- same size, likely CRLF only"
        print(f"  {fn}: {'SAME' if same else 'DIFF'}  local={sa}b LIVE={sb}b{hint}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    global ROOT
    ROOT = find_repo_root(os.getcwd())
    for folder in sys.argv[1:]:
        verify(folder)


if __name__ == "__main__":
    main()
