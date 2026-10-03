# Portal submission notes: Municipality Tycoon

Everything a game portal's submission form is likely to ask for. Check each portal's current rules before submitting, since requirements differ.

## Listing text

**Title:** Municipality Tycoon

**Tagline (about 60 characters):** Run a city council. Approve it, block it, survive it.

**Short description (about 150 characters):** You are the mayor of Clifton. Hear developers, balance the budget, and decide what gets built, before the voters recall you.

**Long description:** (update the lines below to match the current game before pasting)
You are the mayor of Clifton. Every other week the city council meets in chambers. Developers pitch projects from a coffee shop to a billion-dollar data center. Residents line up at the podium. Your own council argues over every condition you attach.

Approve a project and it moves through permitting, construction and operation, and things go wrong or right: unpermitted wells, contaminated water, blackouts, water main breaks, but also new parks, roads and donations. Set the tax rate and fund your departments. Take a council member to lunch. Hear the city attorney's advice, and decide whether to trust it. Resist the lobbyist's envelope, or don't, and hope it never leaks.

Your goal: keep the job and grow Clifton past its population target by the end of your term. Pick a background (business owner, union organizer, teacher, retired cop) and a starting scenario (sleepy town, boom town, town in debt, storm recovery), meet a council whose personalities change every game, and watch the Clifton Courier put your worst moments on the front page.

Play a quick 12-week term in about an hour, or the full 52-week term. There is no single right way to run a city, only trade-offs you have to live with.

**Features**
- Council meetings with a mayor, five council members, citizens at the podium, and staff comments from Zoning and the Fire Marshal
- Randomized conditions for every project, with good options, developer-friendly traps and uncertain wildcards
- Dozens of project incidents, each with its own set of responses, and 16 city-wide crises
- A real budget: property tax, four departments, bonds and deficits
- Council relationships, story arcs, and developers who remember how you treated them
- Bribes that can leak, recall elections, and a city that grows with your decisions
- Sewer plant and landfill that fill up as the city grows, with expansion fights, overflows and recycling programs
- Solar and wind farms that help the grid and hurt the land; surveillance camera networks that catch criminals and cause wrongful arrests; a Police Chief with opinions
- Off-week scenes with a tower crane and moving construction crews, buildings that rise each time you visit, and wealthy, middle-class or struggling neighborhoods on your community walks
- The Clifton Courier: gaffes by you or the council can make the front page, with a snap poll of residents and a reporter who asks about it later
- A final-edition epilogue with a grade, a then-and-now table, 14 achievements and a share card
- A city map with every project and utility, history charts, and a hall of fame
- A Planning Commission that reviews projects first, a mid-term election where challengers can replace council members, and interest groups that endorse you
- Schools, rents and homelessness, fire and EMS response times, parks, transit, fiber and public health
- Town halls where promises you make come due, referendum petitions, state mandates and grants, and federal disaster aid
- Difficulty settings, a daily challenge, and an endless mode in the full version
- Plays on phones as well as desktops, with text size, color-blind and reduce-motion options
- Autosaves every week

## Controls

- **Click, Space or Enter:** advance dialogue
- **F:** change dialogue speed. **A:** auto-advance
- Everything else is clickable buttons. Nothing requires a keyboard or mouse beyond clicking.

## Tags and category

- **Category:** Simulation, strategy
- **Tags:** city, mayor, politics, management, tycoon, simulation, choices, dialogue, humor, singleplayer
- **Players:** single player
- **Language:** English
- **Session length:** about an hour for the quick term, several hours for the full term

## Content notes

- No violence on screen. A few events mention accidents or serious incidents in text (a worker injury, a traffic fatality, a spill), handled seriously.
- Political and civic themes: bribery, corruption, protests, recalls. No real people, parties or places.
- No profanity. No gambling mechanics (a casino is just one project type).
- Suitable for teens and up.

## AI disclosure

Portals now ask about generative AI. For this project the honest answer is **Yes**. The game's code, writing, dialogue, and the guide were produced with an AI tool (Claude, by Anthropic) working with the developer. There is no image or audio art: the characters and scenes are drawn in code, and the sound effects are synthesized in the browser. Suggested wording for a description:

> Made with the help of generative AI. The game's code, writing, and dialogue were produced with Claude, an AI model, under the developer's direction. All visuals are drawn in code and all sounds are synthesized, with no AI image or audio generators.

## Technical facts

- HTML5, a single file (`index.html`), about 280 KB, no external requests, no libraries
- Runs in an iframe. The layout scales to fit the frame with no page scrolling, and falls back to a normal scrolling page when opened directly
- Audio uses the Web Audio API and starts only after the player clicks. It pauses when the tab is hidden. A mute button and volume slider are built in
- Saves use `localStorage`, wrapped so the game still runs if storage is blocked (saving is simply unavailable)
- Desktop and phone browsers. Under 820px wide the layout switches to a phone mode (scaled council scene, one Menu button, larger touch targets). On itch.io tick Mobile friendly (portrait) in the embed options
- Recommended frame size: 960x540 or larger. It runs down to about 800x500, though text gets small at that size

## Assets

- `portal/screens/01-title.jpg` through `05-budget.jpg` are earlier 800x600 screenshots. `06` to `11` show the newer features: title options, Courier front page, construction site, struggling neighborhood, epilogue and the phone layout
- Most portals want specific cover sizes (for example 512x384 and 512x512). Crop or re-capture from the game at those sizes before submitting

## Monetization notes

- The free build can hold rewarded video ads later. Hooks have not been added yet, since each portal uses its own SDK
- The portal build hides every link to the paid version, since portals usually do not allow external purchases

## Before you submit

- Decide whether the portal build should have the Feedback button open an outside form. The button currently copies feedback text and does not leave the page, which portals prefer
- Use the portal build (`python tools/build_itch.py portal`, output in `dist/itch-portal/`): 12-week term only, no outside purchase or tip links. The `GATING` and `EDITION` constants are stamped by the build script
- Test the game in an iframe on the portal's staging page if they offer one
