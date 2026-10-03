# itch.io launch notes

The plan from your notes: put the game on itch.io first, free with a voluntary tip jar, gather feedback, then pitch it to a portal like CrazyGames once it is polished.

## Build the upload

```
python tools/build_itch.py
```

This writes `dist/municipality-tycoon-itch.zip` with `index.html` at the root, which is what itch.io requires for an HTML5 game.

## Page settings

1. Create a new project on itch.io. **Kind of project:** HTML.
2. Upload `dist/municipality-tycoon-itch.zip` and tick **This file will be played in the browser**.
3. **Embed options:** viewport 1280 by 720, turn on the fullscreen button, leave "Mobile friendly" off. The game scales to fit whatever frame you choose.
4. **Pricing:** choose **$0 or donate** (name your price). Set the minimum to $0 and a suggested price of a few dollars. Players can launch the game without paying, and a tip jar sits on the page.
5. Turn on **Donations** if you want players to be able to tip without buying anything.
6. Paste the text from `portal/SUBMISSION.md` for the description, tags and content notes. Use the screenshots in `portal/screens/` for the page gallery.

## Pushing updates with butler

Butler (itch.io's command-line uploader) is installed at `C:\Users\Stephen\butler\butler.exe` and logged in to your account. After you create the project page once (you can upload the zip by hand the first time, or skip that and push straight away):

1. Create a file named `.itch-target` in the repo root containing one line: `yourname/municipality-tycoon:html5` (your itch username, the page's URL slug, and the channel name `html5`). It is ignored by git.
2. Push: `python tools/push_itch.py`. Add `--dry-run` first if you want to see what would be uploaded.

Each push builds the game, uploads only what changed, and tags the build with the current git commit. Pushed updates show up on the itch page after itch processes them, usually within a minute or two. If the page is still a draft, players cannot see it until you make it public.

## In-game tip button

The game has a "Buy the Dev a Coffee" button in the top bar next to Menu. It stays hidden until you give it a link:

- In `index.html`, set `TIP_URL` (near `FEEDBACK_URL`) to your Ko-fi, Patreon, or Stripe checkout link.
- The button hides itself inside iframes, since itch.io and game portals have their own tip and payment features. Players on your own site (the GitHub Pages copy) will see it.
- A short reminder also appears when a player unlocks faster text speeds after their first 12-week term, and on the end-of-term screen.

## Speed unlock

Faster text speeds (2x, 4x, max) stay locked until a player finishes their first 12-week term. After that they unlock permanently in that browser. Players on itch.io will see this the same way.

## Feedback

Itch.io pages have comments and devlogs. Link the playtest notes you gather from friends into the first devlog post, and ask players to use the in-game Feedback button.
