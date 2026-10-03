"""Build the game and push it to itch.io with butler.

Setup (once):
  1. butler is installed at C:\\Users\\Stephen\\butler\\butler.exe and you have run `butler login`.
  2. Create a file named .itch-target in the repo root containing user/game:html5
     for example:  yourname/municipality-tycoon:html5
     (or set the ITCH_TARGET environment variable)

Usage:
  python tools/push_itch.py            push a new build
  python tools/push_itch.py --dry-run  show what would be pushed
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUTLER = os.environ.get("BUTLER") or (r"C:\Users\Stephen\butler\butler.exe" if os.path.exists(r"C:\Users\Stephen\butler\butler.exe") else "butler")

def target():
    t = os.environ.get("ITCH_TARGET")
    if t:
        return t.strip()
    path = os.path.join(ROOT, ".itch-target")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read().strip()
    sys.exit("No target. Create .itch-target containing user/game:html5, or set ITCH_TARGET.")

def main():
    t = target()
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "build_itch.py")])
    try:
        ver = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        ver = "local"
    cmd = [BUTLER, "push", os.path.join(ROOT, "dist", "itch"), t, "--userversion", ver]
    if "--dry-run" in sys.argv:
        cmd.append("--dry-run")
    print(" ".join(cmd))
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
