# Design (Google Stitch)

**Stitch project:** https://stitch.withgoogle.com/projects/9828801172742432808

The screens were generated with the prompts in [`../stitch/PROMPTS.md`](../stitch/PROMPTS.md), one after another in the same Stitch project. Stitch also produced a design system called **Nocturnal Dispatch Console**.

![Overview of the Stitch project](00-stitch-overview.png)

| Screen | Image | Stitch code | In the app |
|---|---|---|---|
| 01 · Intro | `01-intro.png` | `01-intro.stitch.html` | Intro screen (`basla`) |
| 02 · Crisis | `02-crisis.png` | `02-crisis.stitch.html` | Crisis scene (`karar-1-a/b`) |
| 03 · End | `03-end.png` | `03-end.stitch.html` | End screen (`son-a/b`, `karne`) |
| 04 · Outcome | `04-outcome.png` | `04-outcome.stitch.html` | Decision outcome (`sonuc-ne-oldu`, `sonuc-neden`) |

The assignment asks for three screens: intro, scene and end. We added a fourth, the decision outcome, because that is where the game teaches.

`DESIGN.stitch.md` is the design system exported from Stitch. The root [`DESIGN.md`](../DESIGN.md) describes the values the app actually uses.

## From design to code: what stayed and what changed

**What stayed**
- All color tokens (navy ground, neon red, cyan, amber, green, violet) and the rule that red is only for alarms and red codes.
- The screen order: status bar, map, progress bar, content.
- Character message bubbles, the three gauge cards, the A/B decision cards, the minute breakdown table and the shift report.

**What we deliberately changed**
- **Headline font:** Stitch's design system suggested Space Grotesk for headlines. We kept Chakra Petch, because its condensed, angular shapes feel more like monitor and command-console equipment.
- **Map:** Stitch drew the map as a realistic city with street names. In the app the map is a fictional grid, and it is live: ambulances move, calls pulse and a closed road appears.
- **Outcome text:** On the outcome screen Stitch invented details that are not in the scenario (a "water main rupture on Main Avenue", "TTL of 24 hours"). The app's text sticks to the scenario in the spec, so the tutor and the eval talk about the same events.
- **Tutor:** Stitch placed the tutor's question directly on the outcome screen. In the app the tutor speaks in a bottom sheet that opens when the player taps "Ask the tutor", because the player should read the outcome first.

**Ideas we took from Stitch**
- Separate cards for "What happened" and "Why it happened" on the outcome screen.
- Showing the full route on the map on the end screen. In the app this is 7-A's trail.
