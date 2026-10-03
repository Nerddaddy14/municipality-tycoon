"""Build the itch.io uploads.
Writes dist/itch-free/ and dist/itch-full/ (folders for butler) plus a zip of each for manual upload.
The EDITION constant in index.html is stamped as 'free' (12-week term, locked extras) or 'full' (everything).
itch.io HTML5 games need index.html at the root.
Usage: python tools/build_itch.py [free|full|both]   (default: both)"""
import os, re, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist")
FILES = ["index.html", "how-to-play.html"]
MARK = re.compile(r"const EDITION='[a-z]+'")

def build(edition):
    folder = os.path.join(OUT, "itch-" + edition)
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    for name in FILES:
        src = os.path.join(ROOT, name)
        dst = os.path.join(folder, name)
        if name == "index.html":
            text = open(src, encoding="utf-8", newline="").read()
            if not MARK.search(text):
                sys.exit("EDITION marker not found in index.html")
            open(dst, "w", encoding="utf-8", newline="").write(MARK.sub("const EDITION='%s'" % edition, text, count=1))
        else:
            shutil.copy(src, dst)
    target = os.path.join(OUT, "municipality-tycoon-%s.zip" % edition)
    if os.path.exists(target):
        os.remove(target)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            z.write(os.path.join(folder, name), name)
    print("Wrote", folder)
    print("Wrote", target, os.path.getsize(target), "bytes")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    for e in (["free", "full"] if which == "both" else [which]):
        build(e)
