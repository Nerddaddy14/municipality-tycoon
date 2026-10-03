"""Record the Courier front-page animation as a GIF for the itch.io page.

Needs: pip install playwright pillow, and Google Chrome (or Edge) installed.
Start the local server first (python -m http.server 8765 in the repo root), then:

    python tools/make_courier_gif.py

Writes portal/courier-animation.gif. Frames are rendered deterministically by pausing the CSS
animation at a chosen time, so the GIF is smooth regardless of machine speed.
"""
import io, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "portal", "courier-animation.gif")
URL = "http://localhost:8765/index.html?fit=1&gif=1"
W, H = 720, 405          # output size
FPS = 25

SETUP = """
async () => {
  document.querySelector('#startBtn').click();
  await new Promise(r => setTimeout(r, 1200));
  const hs = document.querySelector('#hs'); if (hs) hs.click();
  await new Promise(r => setTimeout(r, 2500));
  window.MUTE = true;
  S.trust = 8;
  const g = {who: 'bradley', quote: 'With respect, not everyone in this room has read a balance sheet.', kind: 'demeaning', flag: ''};
  window.__el = showPaper(g, 'outrage', {outrage: 17, laugh: 1, shrug: 2, cheer: 0}, 20);
  return true;
}
"""

SET_T = """
(t) => {
  const el = document.querySelector('#paper'); if (!el) return;
  const np = el.querySelector('.np');
  el.classList.remove('out');
  el.style.animation = 'none';
  el.style.opacity = Math.min(1, t / 0.25);
  np.style.animation = 'paperin 1s cubic-bezier(.2,.9,.3,1) both paused';
  np.style.animationDelay = (-Math.min(t, 1)) + 's';
}
"""

FADE_T = """
(t) => {
  const el = document.querySelector('#paper'); if (!el) return;
  el.style.opacity = Math.max(0, 1 - t / 0.5);
}
"""

HIDE = "() => { const el = document.querySelector('#paper'); if (el) el.style.display = 'none'; }"

def shot(page):
    png = page.screenshot(type="png")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    return im.resize((W, H), Image.LANCZOS)

def main():
    frames, durs = [], []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(URL)
        page.wait_for_timeout(500)
        page.evaluate(SETUP)
        page.wait_for_timeout(300)
        # background only (no paper): hold briefly at the start
        page.evaluate(HIDE)
        page.wait_for_timeout(100)
        frames.append(shot(page)); durs.append(500)
        page.evaluate("() => { const el = document.querySelector('#paper'); if (el) el.style.display = ''; }")
        # spin-in: 1.0 s
        n = int(FPS * 1.0)
        for i in range(n + 1):
            t = i / n
            page.evaluate(SET_T, t)
            frames.append(shot(page)); durs.append(int(1000 / FPS))
        # hold: 2.2 s (two frames with long durations keeps the file small)
        frames.append(shot(page)); durs.append(2200)
        # fade out: 0.5 s
        n = int(FPS * 0.5)
        for i in range(1, n + 1):
            page.evaluate(FADE_T, i / n)
            frames.append(shot(page)); durs.append(int(1000 / FPS))
        page.evaluate(HIDE)
        frames.append(shot(page)); durs.append(700)
        browser.close()
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=96, dither=Image.FLOYDSTEINBERG) for f in frames]
    pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=1)
    print("Wrote", OUT, os.path.getsize(OUT) // 1024, "KB,", len(frames), "frames")

if __name__ == "__main__":
    main()
