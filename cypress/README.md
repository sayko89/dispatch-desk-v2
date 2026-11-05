# End-to-end tests (Cypress)

| File | Contents |
|---|---|
| `e2e/paths.cy.js` | All 8 decision paths (P1–P8). Each checks the arrival minute, the ending (A/B), the minute breakdown and the KVKK epilog |
| `e2e/acceptance.cy.js` | The acceptance examples AE-1 … AE-5 from `spec.md` |
| `e2e/demo.cy.js` | About one minute of full gameplay (path P5) for the demo video |
| `support/e2e.js` | Shared commands: `startGame`, `finishLivePhase`, `decide`, `continue` |

The tests open the game at `index.html#test`. In test mode the simulation runs 4× faster. The game's rules and numbers don't change.

## Running

```bash
npm install              # installs Cypress (takes a few minutes the first time)
npm run test:e2e         # 8 paths + 5 acceptance examples, headless
npm run cy:open          # watch the tests one by one in the Cypress window
npm run demo             # 60-second demo video
```

The video is saved as `cypress/videos/demo.cy.js.mp4`. Upload it (for example as an unlisted YouTube video) and add the link to the main README.

## How the acceptance examples are tested

| AE | Test | How |
|---|---|---|
| AE-1 | A new player sees hints | Choose "Just starting". The live phase and Crisis 1 show a hint card, and there is no timer |
| AE-2 | An experienced player runs out of time | `cy.clock()` puts the game on a fake clock and 61 s pass on Crisis 1. The system picks the cache, and the ETA becomes 9 min |
| AE-3 | The best path | B-A-A: on time, 7 min, clean KVKK audit |
| AE-4 | The delay breakdown | A-B-A: 13 min, with "Cache +5 min" and "Adding servers +4 min" on separate rows |
| AE-5 | The tutor doesn't give the answer away | The student asks for the answer. The reply contains a question and no "A was right" style verdict |

The tests use the repository's `index.html`, which has no Gemini connection, so the tutor uses scripted replies and AE-5 gives the same result on every run. The real model's behavior is measured in `eval/`.

## Verification

After the tests were written, the same steps and selectors were replayed with Playwright against the game. All 8 paths and AE-1, AE-2, AE-4 and AE-5 passed. AE-3 has the same expectations as P5, so it is covered too. One path takes about 35 seconds, and the full suite about 7–8 minutes when run in sequence.
