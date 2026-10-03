# Municipality Tycoon

A city council simulator. You are the mayor of Clifton: every other week the council meets, you work through an agenda (a budget hearing every six weeks, small items, and one main development proposal), attach conditions, take votes, and deal with what gets built. Off weeks are for inspections, resident meetings, lunches with council members, press, and private meetings with developers.

Playtest build. Open the page and press "Call the meeting to order". The game autosaves at the start of every week.

## Systems

- Council of five with relationships, favors, and votes you have to earn
- Weekly finances: property tax rate, department funding, bonds, deficits and state oversight
- City growth: population, housing supply, traffic
- Ordinances that apply to future projects
- Staged projects with incidents (wells, contamination, noise, blackouts, water main breaks)
- Crises (heat waves, droughts, floods, cyber attacks, scandals, housing protests)
- Recall elections with challengers and campaigning
- City attorney advice that may be good or bad, staff reports, closed-door meetings, bribes and leaks
- Developers with personalities and track records, council story arcs, seasonal festivals, quarterly priorities, and a pool of 16 non-repeating crises plus dozens of project events

## Free and paid versions

`index.html` ships fully unlocked (`const GATING=false`). Set `GATING=true` to enforce the split:

- Free: 12-week term, one autosave slot, classic chambers, base projects, no recall elections
- Full: 52-week term, recall elections, chamber themes, project packs (Entertainment, Energy), dialogue packs, 3 manual save slots

Keys look like `MT-XXXX-XXXX-CHECK` and are generated with `python tools/make_license.py 5`. They are checked in the browser, so they only deter casual copying. For real protection, sell the full game as a separate build or validate keys on a server.

## Tools

`tools/sim-harness.js` runs the game headless in the browser for balance and pacing checks. Serve the folder (`python -m http.server`), open the page, then evaluate the harness in the console and run `await SIM.batch(12, 20, 'sensible')` or `await SIM.batch(52, 10, 'random')`.

## Feedback

Players use the Feedback button in the game. To collect responses in a form, set `FEEDBACK_URL` near the bottom of `index.html`.
