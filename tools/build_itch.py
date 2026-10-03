"""Build the itch.io upload.
Writes dist/itch/ (a folder for butler) and dist/municipality-tycoon-itch.zip (for a manual upload).
itch.io HTML5 games need index.html at the root.
Usage: python tools/build_itch.py"""
import os, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist")
FILES = ["index.html", "how-to-play.html"]

folder = os.path.join(OUT, "itch")
if os.path.isdir(folder):
    shutil.rmtree(folder)
os.makedirs(folder)
for name in FILES:
    shutil.copy(os.path.join(ROOT, name), os.path.join(folder, name))

target = os.path.join(OUT, "municipality-tycoon-itch.zip")
if os.path.exists(target):
    os.remove(target)
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for name in FILES:
        z.write(os.path.join(ROOT, name), name)
print("Wrote", folder)
print("Wrote", target, os.path.getsize(target), "bytes")
