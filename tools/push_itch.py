"""Build the game and push it to itch.io with butler.

Two itch pages, two builds:
  free  -> the free 12-week page      (target in .itch-target,       e.g. nerddaddy/municipality-tycoon:html5)
  full  -> the paid 52-week page      (target in .itch-target-full,  e.g. nerddaddy/municipality-tycoon-full:html5)
(or set ITCH_TARGET / ITCH_TARGET_FULL environment variables)

Usage:
  python tools/push_itch.py free             push the free build
  python tools/push_itch.py full             push the paid build
  python tools/push_itch.py both             push both
  add --dry-run to any of them to see what would be pushed
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUTLER = os.environ.get("BUTLER") or (r"C:\Users\Stephen\butler\butler.exe" if os.path.exists(r"C:\Users\Stephen\butler\butler.exe") else "butler")
TARGETS = {"free": (".itch-target", "ITCH_TARGET"), "full": (".itch-target-full", "ITCH_TARGET_FULL")}

def target(edition):
    fname, env = TARGETS[edition]
    t = os.environ.get(env)
    if t:
        return t.strip()
    path = os.path.join(ROOT, fname)
    if os.path.exists(path):
        return open(path, encoding="utf-8").read().strip()
    sys.exit("No target for the %s build. Create %s containing user/game:html5, or set %s." % (edition, fname, env))

def push(edition):
    t = target(edition)
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "build_itch.py"), edition])
    try:
        ver = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        ver = "local"
    cmd = [BUTLER, "push", os.path.join(ROOT, "dist", "itch-" + edition), t, "--userversion", ver]
    if "--dry-run" in sys.argv:
        cmd.append("--dry-run")
    print(" ".join(cmd))
    return subprocess.call(cmd)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    which = args[0] if args else "free"
    if which not in ("free", "full", "both"):
        sys.exit("Use: free, full or both")
    code = 0
    for e in (["free", "full"] if which == "both" else [which]):
        code = push(e) or code
    sys.exit(code)

if __name__ == "__main__":
    main()
