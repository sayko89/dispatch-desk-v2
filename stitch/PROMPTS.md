# Stitch prompts

In Stitch, **create a new project** and choose **Mobile** as the device. Generate the three screens **in the same project, one after another**, so Stitch carries the style of the first screen over to the next ones.

Paste each prompt exactly as it is.

When the screens are done:
1. Export each screen as a PNG into the repository's `design/` folder: `01-intro.png`, `02-crisis.png`, `03-end.png`.
2. If Stitch offers a DESIGN.md export, save it as `design/DESIGN.stitch.md`. The root `DESIGN.md` holds the values the app really uses, and keeping both side by side shows what changed between design and code.
3. Add the Stitch project's share link to the README.

---

## 0 · Style (paste once, at the start of the first prompt)

```
Design system for all screens: a dark "hospital monitor at night" look for a mobile ambulance dispatch game called Dispatch Desk.
Colors: background #030920, cards #0A1636, raised surfaces #0F1E47, borders #1A2C60, text #E9F1FF, secondary text #8598C8.
Accents: neon red #FF2D55 only for alarms, red-code patients and the primary button (with a soft red glow); cyan #25E2FF for system state, stations and ambulances; amber #FFC53D for yellow code, warnings and hints; green #22F0A3 for green code and success; violet #AE8FFF for privacy topics.
Fonts: Chakra Petch for titles and big numbers, IBM Plex Sans for dialogue and body text, JetBrains Mono for clocks, IDs, labels and chips.
Cards have 12px radius and 1px borders instead of shadows. Only neon elements glow. No emoji, no photos, no light theme. Single column, 390px wide phone.
```

## 1 · Intro screen

```
Screen 1: Intro / start screen of Dispatch Desk.

Top: a small neon red plus-shaped medical cross next to a mono uppercase label "112 COMMAND CENTER · NIGHT SHIFT".
Huge two-line uppercase title: "DISPATCH" in white and "DESK" in neon red with a strong red glow.
One paragraph: "Friday night, 21:32. Six ambulances, three stations and three hospitals are on your screen. Soon the map service will slow down and a red-code call will come in."
A thin red ECG heartbeat line across the width.

Below it, a live city map card (rounded, navy grid of streets, a diagonal dark-blue river with two bridges labeled N. BRIDGE and S. BRIDGE). On the map: three cyan outlined squares labeled STN 7, STN 5, STN 3; three red rounded squares with white crosses labeled Haydarpaşa, Kadıköy State, Göztepe Hosp., each with a small capacity bar; a few glowing white ambulance dots with cyan trails; small green and amber call dots with pulsing rings. A "LIVE" tag with a blinking red dot in the corner.

Then a form with three groups of pill-shaped segmented buttons:
- "Your level" (small grey note: "the story adapts to it"): Just starting / Know a bit (selected, red outline with glow) / Experienced. Helper text under it.
- "Your role": Developer (selected) / Test engineer / Product manager.
- "Your goal": Architecture (selected) / Scaling / Data privacy.

A "ON SHIFT TONIGHT" label and a 2-column list of six characters, each with a round colored avatar letter and name + role: Derya, dispatch supervisor (amber); Kaan, on-call SRE (cyan); Ece, test engineer (green); Burak, product manager (orange); Selin, data protection officer (violet); Dr. Mert, on-call ER physician (red).
A mono facts row: 6 ambulances · 3 stations · 3 hospitals · 3 crises · 5 field tasks.
Full-width neon red primary button: "Take the shift".
Small grey footer: "Prototype. The city, people and cases are fictional."
```

## 2 · Crisis screen

```
Screen 2: Crisis decision screen, same style.

Sticky top status bar: clock "21:40:03" in mono with a faint cyan glow, a tiny red ECG trace, two small counters "ACTIVE 2" and "FREE 1/6", and on the right a red outlined glowing pill "K-114 · target 10 min".

Below, the same live map card, now in a degraded state: a dim overlay, a red outlined box "Map data delayed · 8.2 s", and a large pulsing red dot labeled "K-114" in the east side. Two small toast notifications at the top left of the map: "Task: Duplicate call" (amber left border) and "RED CODE · K-114 Kadıköy" (red left border).

A 6-segment progress bar (first segment cyan, second red and glowing) with mono text "Part 2/6 · Crisis 1" and "Target: K-114 in 10 min".

Three chat-style message bubbles, each with a round avatar letter and a mono "Name · role" line in the character's color:
- Kaan · on-call SRE (cyan K): "You're on call. The map API's p95 response time is 8.2 seconds and the routing screen is freezing."
- Derya · dispatch supervisor (amber D): "K-114: Kadıköy, chest pain, age 58. Advanced life support crew 7-A at Station 7 is ready but has no route."
- Dr. Mert · on-call ER physician (red M): "The cardiac team at Kadıköy State is getting ready. We need the patient within 10 minutes."

A row of three small gauge cards: "MAP API P95 · 8.2 s" in red with a rising red sparkline and red border; "ERROR RATE · 14%" in amber with an amber sparkline; "CACHE AGE · 3.7 h" with caption "last updated yesterday 18:00".

Red mono eyebrow "CRISIS 1 / 3 · ARCHITECTURE" (the word ARCHITECTURE in cyan).
Big title: "Which map should 7-A leave with?"
Two large decision cards stacked, each with a big glowing red letter on the left:
- A · "Use the cached map" / "Loads instantly. Last updated: yesterday 18:00."
- B · "Fail over to the backup provider" / "Switching takes 3 minutes. The data is current."
At the bottom, a hint box with a dashed amber border, amber "HINT" label and: "Check when the cache was last updated. What could have changed in the city since then?"
```

## 3 · End screen

```
Screen 3: End / result screen, same style.

Same sticky status bar, the pill now reads "Arrived · 13 min" in red with glow.
The live map card shows the full red route of ambulance 7-A, a blinking red X labeled "CLOSED" on one street, a hospital marked "NOT ACCEPTING", and violet dots along the route with a violet tag "→ ANALYTICS: RAW TRAIL".
Progress bar fully cyan: "Part 6/6 · Crisis 3".

Mono eyebrow "CASE CLOSED · PATH P4".
Huge uppercase title "DELAYED" in neon red with glow.
Giant number "13" with a small grey "min" next to it, and mono caption "Target: 10 minutes or less".
One sentence: "The ambulance arrived in 13 minutes. The target was 10. The patient survived, but treatment was delayed."

A card "Where the minutes came from" with a ledger table, right column in mono:
Base arrival time (If the system had worked normally) 4 min · Cache (Crisis 1 · Architecture) +5 min · Adding servers (Crisis 2 · Scaling) +4 min · Raw data kept forever (Crisis 3 · Data and privacy) ±0 min · Total 13 min (bold).

A card "One week later" with a red left border: "A KVKK (data protection) audit found raw location records kept indefinitely. An incident report was opened and the data controller was notified."

A card "Shift report" with a large cyan glowing score "90/100", three small stat tiles ("10/10 calls got a crew", "100% closest crew picked", "0.5 min average to assign"), and a task list with green ✓ or red ✗ marks: Duplicate call ✓, Hospital full ✓, Public statement ✓, Lost signal ✓, Skipped test ✗. Each item has a one-line grey lesson under it.
Full-width neon red button "Play again".
```

---

## Tips

- If Stitch colors something wrong (for example makes links red), ask for just that fix: *"Keep red only for alarms and the primary button. Make links amber."*
- Stitch will draw the map as a simple illustration, which is fine. The real map is drawn with canvas in the app. The point of the design is to show layout and visual language.
- Make sure all three screens use the same status bar and map. If Stitch makes them different, say *"Use exactly the same status bar and map card as screen 2."*
