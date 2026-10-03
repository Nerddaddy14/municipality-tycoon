"""Build the itch.io upload: dist/municipality-tycoon-itch.zip
itch.io HTML5 games need index.html at the root of the zip.
Usage: python tools/build_itch.py"""
import os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist")
FILES = ["index.html", "how-to-play.html"]

os.makedirs(OUT, exist_ok=True)
target = os.path.join(OUT, "municipality-tycoon-itch.zip")
if os.path.exists(target):
    os.remove(target)
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for name in FILES:
        z.write(os.path.join(ROOT, name), name)
print("Wrote", target, os.path.getsize(target), "bytes")
