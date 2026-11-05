# DESIGN.md · Dispatch Desk

> Design system for **SE Primer: Dispatch Desk**, a mobile story game about an ambulance dispatch center.
> Every value below is taken from the shipped app (`index.html`), so the Stitch screens, the AI Studio app and the Cypress tests describe the same product.

## 1. Concept

**A hospital monitor at night.** The player sits at a dispatch console during a Friday night shift. The screen should feel like ICU and command-center equipment: a deep navy background, a single neon red reserved for alarms and red-code patients, cyan for system and machine state, and dense monospaced data next to calm, readable body text.

Three rules shape every screen:

1. **Red means danger, nothing else.** Red is used for red-code patients, alarms, closed roads, crisis labels and the primary action. If something is red, the player should feel urgency.
2. **The map is always visible.** In-game screens keep the live city map near the top. The story happens on it: ambulances move, calls pulse, a closed road blinks.
3. **Data in mono, story in sans.** Numbers, clocks, IDs and labels use the mono face. Dialogue, choices and explanations use the body face.

**Theme:** dark only, on purpose. The game is set at night and the neon accents depend on a dark ground.

## 2. Color tokens

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#030920` | Page background |
| `--bg-2` | `#06102C` | Map background, inset areas |
| `--panel` | `#0A1636` | Cards, bubbles, queue rows |
| `--panel-2` | `#0F1E47` | Buttons, choice cards, raised surfaces |
| `--line` | `#1A2C60` | Default borders, dividers |
| `--line-2` | `#27438A` | Stronger borders, button outlines |
| `--fg` | `#E9F1FF` | Primary text |
| `--muted` | `#8598C8` | Secondary text, labels |
| `--dim` | `#50659A` | Tertiary text, map captions |
| `--red` | `#FF2D55` | Alarm, red code, primary button, crisis label |
| `--cyan` | `#25E2FF` | System state, stations, ambulances, focus ring |
| `--amber` | `#FFC53D` | Yellow code, warnings, hints, tasks |
| `--green` | `#22F0A3` | Green code, success, "on time" |
| `--violet` | `#AE8FFF` | Data and privacy, hospital transport |
| `--orange` | `#FF8F3F` | Product manager character |
| `--pink` | `#FF6FA8` | Tutor |
| `--river` | `#0A2352` | River on the map |
| `--road` | `#13265A` | Roads on the map |

**Glows.** Neon elements carry a soft glow in their own color: `--red-glow rgba(255,45,85,.55)`, `--cyan-glow rgba(37,226,255,.45)`. Glow is applied with `text-shadow` or `box-shadow`, never as a blurred background block.

**Triage codes** are semantic and never reused for decoration:

| Code | Color | Chip |
|---|---|---|
| Red | `--red` | Solid red, white text |
| Yellow | `--amber` | 16% amber fill, amber text |
| Green | `--green` | 14% green fill, green text |

**Characters** each own one color, used for the avatar and the name in message bubbles:

| Character | Role | Color |
|---|---|---|
| Derya | Dispatch supervisor | Amber |
| Kaan | On-call SRE | Cyan |
| Ece | Test engineer | Green |
| Burak | Product manager | Orange |
| Selin | Data protection officer | Violet |
| Dr. Mert | On-call ER physician | Red |
| Tutor | Socratic tutor | Pink |

## 3. Typography

| Role | Family | Weights | Use |
|---|---|---|---|
| Display | **Chakra Petch** | 600, 700 | Game title, screen titles, crisis questions, big numbers |
| Body | **IBM Plex Sans** | 400, 500, 600 | Dialogue, choices, explanations |
| Data | **JetBrains Mono** | 400, 500, 700 | Clock, IDs, labels, chips, map captions, radio log |

Fallbacks: `"Arial Narrow", system-ui` for display, `system-ui, -apple-system, Roboto` for body, `ui-monospace, Menlo, Consolas` for data.

| Style | Size / line height | Notes |
|---|---|---|
| Hero title | 46–64px / 0.9, uppercase | "DISPATCH" in white, "DESK" in neon red with glow |
| Outcome title | 46px / 1, uppercase | "ON TIME" green or "DELAYED" red, with glow |
| Big number | 80px / 0.9 | Arrival minutes on the end screen, tabular numerals |
| Screen title | 26px / 1.1 | `text-wrap: balance` |
| Choice title | 16px / 600 | |
| Body | 15px / 1.5 | |
| Eyebrow label | 10.5px mono, uppercase, letter-spacing 0.14em | Section labels such as "CRISIS 1 / 3 · ARCHITECTURE" |
| Chip | 9.5px mono, uppercase | Triage codes |

All numbers that line up (clock, ETA, minutes, scores) use `font-variant-numeric: tabular-nums`.

## 4. Layout and spacing

- **Single column, phone first.** Max content width 480px, centered. Side gutter at least 16px, plus the device safe area.
- **Vertical rhythm.** Sections are separated by 14px. Items inside a section by 8–12px. Spacing comes from `gap`, not margins.
- **Radius.** Cards 12px, map 14px, buttons 10px, chips 4px, pills 999px, bottom sheet 18px on the top corners.
- **Borders over shadows.** Surfaces are separated by 1px borders in `--line`. Only neon elements (alarm, primary button, red ETA pill) get a colored glow.

### In-game screen order (top to bottom)
1. Sticky status bar
2. Live map
3. Map legend
4. Progress bar (6 parts)
5. Screen-specific content

## 5. Components

### Status bar (sticky)
Clock `21:40:03` in mono with a faint cyan glow · small red ECG trace · "ACTIVE" and "FREE" counters · ETA pill on the right. The pill states are: grey "No K-114", red "K-114 · target 10 min", amber or green "ETA ~9 min", and green or red "Arrived · 13 min".

### Live map
A 364×248 canvas. A navy grid city split by a diagonal river with two bridges. Stations are cyan outlined squares with a number. Hospitals are red rounded squares with a white cross and a capacity bar beneath. Calls are glowing dots in their triage color with a pulsing ring while waiting. Ambulances are white dots with a cyan glow, a fading trail and alternating red/cyan siren lights. The red-code ambulance 7-A has a red ring. Overlays: toasts top left (mono, colored left border), a "LIVE" tag with a blinking red dot bottom right, and a red "Map data delayed · 8.2 s" box while the map service is slow.

### Progress bar
Six equal segments: Handover, Crisis 1, Surge, Crisis 2, Field, Crisis 3. Done segments are cyan, the current one is red with a glow.

### Message bubble
A 30px round avatar with the character's initial, then a bubble (`--panel`, radius 4/12/12/12) with "Name · role" in mono in the character color, followed by the message.

### Call card (live dispatch)
A left border in the triage color, then a chip, call ID, neighborhood and status ("waiting 1.2 min", "5-B en route"). The complaint goes on the second line. Tapping opens a crew picker with each crew's ID, type, location and estimated arrival. The closest crew gets a green "closest" tag, and 7-A shows as locked ("red-code reserve").

### Fleet grid
Three columns, six cells, one per ambulance. Each cell shows the ID, ALS/BLS type and a colored status: Available (green), En route (cyan), On scene (amber), At hospital (violet), Red-code mission (red border with glow), No signal (amber, blinking).

### Task card
An amber border with a soft amber glow. It shows a "TASK · title" eyebrow, the character's message and two options labeled A and B. When resolved it turns into a quiet card with the consequence.

### Alarm card
A red border and red glow with a moving dashed red stripe on top. Inside: a red title, one paragraph and a full-width primary button ("Go to the crisis").

### Gauges
Three cells in a row, each with a mono label, a large value and either a sparkline or a short caption. A red gauge gets a red border and a red value with glow.

### Decision card
A large red "A" or "B" letter with glow, then the option title and a one-line consequence hint. On hover or focus the border turns red and glows.

### Hint and timer
**Hint:** a dashed amber border with an amber "HINT" eyebrow.
**Timer** (experienced level): a thin bar that turns from cyan to red in the last 15 seconds, with the seconds remaining in mono.

### Outcome block
A large delta ("+5 min" amber, "+4 min" red, "+0 min" green), then "What happened" and "Why it happened" cards. When the player's goal matches the decision's topic, the second card has an extra expanded section.

### End screen
The outcome title, the big minute count, a ledger table ("Where the minutes came from") and an epilog card. The epilog has a violet left border if the privacy audit passed and a red one if it failed. Below it sits the shift report: a 0–100 score in cyan, three stat tiles and a task list with ✓ or ✗ plus one lesson line per task.

### Tutor sheet
A bottom sheet over a dark scrim. Tutor bubbles use the pink "T" avatar and the label "gives hints, not answers". Quick replies appear as pills, with a text input and a send button below.

### Buttons
| Type | Style |
|---|---|
| Primary | Red fill, white text, red glow |
| Secondary | `--panel-2` fill with a `--line-2` border that turns cyan on hover |
| Link | Amber underlined text |

## 6. Motion

- Map: continuous (moving traffic, a slow cyan scanline, pulsing call rings, sirens).
- Messages rise in one after another with 0.2s steps.
- The alarm stripe slides and the LIVE dot blinks.
- Everything respects `prefers-reduced-motion`: pulses, scanline and sirens stop, and the ambulance jumps to its destination.

## 7. Accessibility

- Text contrast: `--fg` on `--bg` is 17.4:1, `--muted` on `--bg` is 6.9:1 and on `--panel` 6.2:1, all above WCAG AA.
- Color is never the only signal. Triage chips carry the words RED, YELLOW and GREEN, and outcomes carry a title as well as a color.
- Visible focus ring: a 2px cyan outline.
- Touch targets are at least 40px tall.

## 8. Screens

| Screen | Purpose | Key components | Test IDs |
|---|---|---|---|
| **Intro** | Pick level, role and goal, then start | Hero, live map, segmented pills, crew list, facts row, primary button | `seviye-*`, `rol-*`, `hedef-*`, `basla` |
| **Live dispatch** | Assign crews, answer tasks | Status bar, map, progress, task card, call cards, fleet grid, radio log, alarm | `cagri-*`, `ekip-*`, `gorev-*`, `krize-gec` |
| **Crisis** | Make one of three decisions | Status bar, map, message bubbles, gauges, decision cards, hint or timer | `karar-n-a/b`, `ipucu-kart`, `sayac` |
| **Outcome** | Show what happened and why | Delta, two explanation cards, tutor and continue buttons | `sonuc-ne-oldu`, `sonuc-neden`, `tutor-ac`, `devam` |
| **End** | Final result and shift report | Outcome title, big number, ledger, epilog, shift report | `son-a/b`, `varis-dk`, `dokum`, `epilog`, `karne`, `bastan` |

Stitch screens: **Intro**, **Crisis** and **End** (the three the assignment asks for), plus **Outcome**. See `design/` for the images, the Stitch export (`DESIGN.stitch.md`) and a note on what changed between design and code. The project: https://stitch.withgoogle.com/projects/9828801172742432808

## 9. Don'ts

- Don't use red for decoration, links or neutral information.
- Don't add a light theme. The neon accents are designed for the dark ground.
- Don't put dialogue in mono or numbers in the body face.
- Don't use emoji or stock medical photos. The only medical symbol is the plain red cross.
- Don't show which option is "correct" anywhere before the end screen.
