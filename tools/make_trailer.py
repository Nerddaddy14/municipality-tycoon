"""Record the Municipality Tycoon trailer (silent, 1280x720 mp4) from the live game.

Needs: pip install playwright imageio-ffmpeg, and Google Chrome (or Edge) installed.
Start the local server first (python -m http.server 8765 in the repo root), then:

    python tools/make_trailer.py [--vertical]

Each scene is recorded in a fresh page, with a caption injected into the page, then the clips are
joined with ffmpeg. Writes portal/trailer.mp4 (or portal/trailer-vertical.mp4, 1080x1920, with --vertical).
"""
import glob, os, shutil, subprocess, sys, tempfile, time
import re
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERT = "--vertical" in sys.argv   # 9:16 cut for Reels / TikTok / Shorts
OUT = os.path.join(ROOT, "portal", "trailer-vertical.mp4" if VERT else "trailer.mp4")
BASE = "http://localhost:8765/index.html" + ("" if VERT else "?fit=1")
VW, VH = (720, 1280) if VERT else (1280, 720)
OW, OH = (1080, 1920) if VERT else (1280, 720)
FF = imageio_ffmpeg.get_ffmpeg_exe()

CAP_JS = """
(text) => {
  const FS = window.innerWidth < 800 ? 46 : 44;
  let c = document.getElementById('cap');
  if (!c) {
    c = document.createElement('div'); c.id = 'cap';
    c.style.cssText = 'position:fixed;left:0;right:0;top:34px;text-align:center;z-index:99999;pointer-events:none;font:800 '+FS+'px/1.15 Georgia,serif;color:#fff;text-shadow:0 3px 14px #000,0 0 3px #000;padding:60px 60px 40px;background:linear-gradient(rgba(0,0,0,.72),rgba(0,0,0,0));top:0;transition:opacity .4s';
    document.body.appendChild(c);
  }
  c.textContent = text;
  c.style.opacity = text ? 1 : 0;
}
"""

PREP = """
() => {
  const st = document.createElement('style');
  st.textContent = `#side{display:none!important}
    body.mob #app{display:flex;flex-direction:column;justify-content:center;padding-top:150px;padding-bottom:40px}
    body{background:radial-gradient(circle at 50% 30%,#1b2740,#080c14)!important}
    body.mob #dlgText{font-size:22px;min-height:84px}
    body.mob #dlg,body.mob #choices{min-height:130px}
    #overlay .box,#modal .box{zoom:1.3}`;
  document.head.appendChild(st);
}
"""

SETUP = """
() => {
  window.MUTE = true;
  S.maxWeeks = 12; newGameSetup();
  document.querySelector('#overlay').classList.add('hidden');
  hud();
}
"""

BOT = """
() => {
  if (window.__bot) return;
  window.__bot = setInterval(() => {
    const c = document.querySelector('#choices');
    if (c && !c.classList.contains('hidden')) {
      const bs = [...c.querySelectorAll('button')];
      if (bs.length) bs[Math.floor(Math.random() * bs.length)].click();
    }
    const m = document.querySelector('#modal');
    if (m && !m.classList.contains('hidden')) { const b = m.querySelector('button'); if (b) b.click(); }
  }, 1100);
}
"""

PROJECTS = """
() => {
  const kinds = [4, 4, 3, 3, 2, 2, 1, 0, 4, 3];
  for (let i = 0; i < kinds.length; i++) {
    const p = genProject(); p.conds = p.conds || {};
    p.stage = kinds[i]; p.stageLeft = kinds[i] < 4 ? 2 : 0;
    S.projects.push(p); S.stats.approved++;
  }
  S.pop = 14200; S.trust = 71; S.env = 62; S.dev = 66; S.budget = 2400000; S.corrupt = 6;
}
"""


def launch(p):
    try:
        return p.chromium.launch(channel="chrome", headless=True)
    except Exception:
        return p.chromium.launch(channel="msedge", headless=True)


def record(name, fn, tmp):
    """Run fn(page) in a fresh recorded page; return the saved webm path."""
    d = os.path.join(tmp, name)
    os.makedirs(d)
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={"width": VW, "height": VH}, record_video_dir=d,
                            record_video_size={"width": VW, "height": VH})
        t0 = time.time()
        page = ctx.new_page()
        page.goto(BASE)
        page.wait_for_timeout(700)
        if VERT:
            page.evaluate(PREP)
            page.wait_for_timeout(300)
        start = time.time() - t0
        fn(page)
        end = time.time() - t0
        ctx.close()
        b.close()
    return glob.glob(os.path.join(d, "*.webm"))[0], start, end


def clip_len(path):
    """Real length of a recorded clip in seconds (the page clock and the video clock can drift)."""
    out = subprocess.run([FF, "-i", path], capture_output=True, text=True).stderr
    h, m, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()
    return int(h) * 3600 + int(m) * 60 + float(sec)


def cap(page, text):
    page.evaluate(CAP_JS, text)


def scene_title(page):
    cap(page, "You are the mayor of Clifton.")
    page.wait_for_timeout(3600)


def scene_council(page):
    page.evaluate(SETUP)
    page.evaluate("() => { SPD = 4; AUTOADV = true; S.week = 3; runGame(); }")
    page.evaluate(BOT)
    cap(page, "Every two weeks, the council votes on what gets built.")
    page.wait_for_timeout(5500)
    cap(page, "Hear the public. Set conditions. Count the votes.")
    page.wait_for_timeout(8500)


def scene_bribe(page):
    page.evaluate(SETUP)
    page.evaluate("""() => { SPD = 4; AUTOADV = true;
      const ap = genProject(); S.agenda = ap;
      const rr = Math.random, q = [0, 0]; Math.random = () => q.length ? q.shift() : rr();
      officeMeeting(ap); }""")
    cap(page, "Behind closed doors, someone slides you an envelope.")
    page.wait_for_function("() => !document.querySelector('#choices').classList.contains('hidden')", timeout=30000)
    page.wait_for_timeout(3200)
    cap(page, "Take it, and hope it never leaks.")
    page.evaluate("() => document.querySelector('#choices button').click()")
    page.wait_for_timeout(5200)


def scene_courier(page):
    page.evaluate(SETUP)
    page.evaluate("""() => { S.trust = 8;
      const g = {who: 'bradley', quote: 'With respect, not everyone in this room has read a balance sheet.', kind: 'demeaning', flag: ''};
      window.__el = showPaper(g, 'outrage', {outrage: 17, laugh: 1, shrug: 2, cheer: 0}, 20); }""")
    cap(page, "Say the wrong thing, and the Courier prints it.")
    page.wait_for_timeout(5600)


def scene_map(page):
    page.evaluate(SETUP)
    page.evaluate(PROJECTS)
    page.evaluate("() => showMap('map')")
    cap(page, "Watch your decisions reshape the town.")
    page.wait_for_timeout(2600)
    page.evaluate("""() => { const z = document.getElementById('mz+'); if (z) { z.click(); z.click(); } }""")
    page.wait_for_timeout(3600)
    page.evaluate("() => { const b = document.querySelector('.chips button[data-m=\"util\"]'); if (b) b.click(); }")
    page.wait_for_timeout(2400)


def scene_epilogue(page):
    page.evaluate(SETUP)
    page.evaluate(PROJECTS)
    page.evaluate("() => { S.week = 13; ending('TERM|You finished your full term as mayor of Clifton.'); }")
    cap(page, "Re-elected? Run out of town? Your call.")
    page.wait_for_timeout(5200)


def scene_end(page):
    page.evaluate("""() => {
      document.querySelector('#overlay').classList.add('hidden');
      const d = document.createElement('div');
      d.style.cssText = 'position:fixed;inset:0;z-index:100000;background:radial-gradient(circle at 50% 40%,#1d2b46,#0a0f1a);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Georgia,serif;text-align:center';
      d.innerHTML = '<div style="font-size:30px;letter-spacing:6px;color:#9fb4d8">THE COUNCIL IS IN SESSION</div><div style="font-size:92px;font-weight:800;margin:14px 0">Municipality Tycoon</div><div style="font-size:36px;color:#ffd77a">Play free in your browser</div><div style="font-size:30px;margin-top:22px;color:#cfe0ff">nerddaddy.itch.io/municipality-tycoon</div>';
      document.body.appendChild(d);
    }""")
    page.wait_for_timeout(3800)


SCENES = [("title", scene_title), ("council", scene_council), ("bribe", scene_bribe),
          ("courier", scene_courier), ("map", scene_map), ("epilogue", scene_epilogue), ("end", scene_end)]


def main():
    tmp = tempfile.mkdtemp(prefix="mt-trailer-")
    clips = []
    for name, fn in SCENES:
        print("recording", name, flush=True)
        clips.append(record(name, fn, tmp))
    inputs, filt, durs = [], [], []
    for i, (c, st, en) in enumerate(clips):
        inputs += ["-i", c]
        en = min(en, clip_len(c) - 0.05)
        durs.append(en - (st + 0.25))
        filt.append(f"[{i}:v]trim=start={st + 0.25:.2f}:end={en:.2f},setpts=PTS-STARTPTS,fps=30,scale={OW}:{OH}:flags=lanczos,format=yuv420p[v{i}]")
    T = 0.55   # crossfade length between scenes
    cur, total = "v0", durs[0]
    for i in range(1, len(clips)):
        out = f"x{i}"
        filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration={T}:offset={total - T:.2f}[{out}]")
        cur, total = out, total + durs[i] - T
    filt.append(f"[{cur}]fade=t=in:st=0:d=0.4[out]")
    cmd = [FF, "-y"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[out]",
           "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    print("Wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
