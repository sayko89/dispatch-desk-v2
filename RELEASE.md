# Release · Dispatch Desk v2.0

## What changed in v2.0

| Area | v1.0 | v2.0 |
|---|---|---|
| Decisions, numbers, endings | 3 crises, 8 paths, 2 endings | **unchanged** (AE-1 … AE-5 and P1–P8 still pass with the model on) |
| Personalization | intro answers only (level, role, goal) | plus a **costly-decision risk model** that reads how the player has played so far |
| What the model changes | – | p ≥ 0.50 → support card on the crisis scene (`destek-kart`) and the expanded explanation on the outcome screen (`sonuc-derin`) |
| Where it runs | – | in the player's browser, onnxruntime-web 1.22.0, model file under 1 KB |
| Data | none kept | 3 anonymous rows per session, kept on the device until the player copies them (end screen, "Research data") |
| New screens | – | Model lab (intro footer), used for the parity test |
| Server | – | optional FastAPI consumer (`server/`, bonus) |

## Pinned model

| | |
|---|---|
| Hugging Face repo | `saiyko/dispatch-desk-risk` |
| Pinned commit | `HF_COMMIT` (filled in after upload) |
| URL used by the app | `https://huggingface.co/saiyko/dispatch-desk-risk/resolve/HF_COMMIT/model.onnx` |
| Fallback | the copy in this repo's `model/` folder, served by GitHub Pages |
| Gate result | see `model/config.json` → `metrics` (ROC AUC ≥ 0.70 required, spec 11.4) |

Consumers pin a commit, never `main`. A new upload to Hugging Face therefore cannot change a running game until we change `MODEL_SRC.hfCommit` in `index.html` and release it.

## Release plan

The stage lives in one constant, `ROLLOUT` in `index.html`. The URL parameter `?rollout=` overrides it for tests and demos. Each session logs its stage in the `rollout` column, so every row says which version the player saw.

| Stage | Setting | What players see | Exit criteria to go to the next stage |
|---|---|---|---|
| 0 · Data collection | `off` | v1 game; rows collected | ≥ 15 real sessions; `train.py` passes the gate |
| 1 · Shadow | `shadow` | v1 game; model runs, p is shown as "shadow" and logged, no support card | p is produced in every session, no console errors, latency < 50 ms; compare p with the actual choices |
| 2 · Canary 5 % | `canary`, `CANARY_PERCENT = 5` | 5 % of sessions get the support card | No new errors; supported sessions do not end worse than the rest; no complaints that the card gives the answer away |
| 3 · Progressive | `CANARY_PERCENT` 25 → 50 → 100 | larger share each step | Same checks at each step, at least a day apart |
| 4 · On | `on` | everyone | – |

**Where this release is.** Stage 0 ran with real players (16 sessions, `rollout = off`). The course has no user base to canary on, so v2.0 ships at stage 4 (`ROLLOUT_DEFAULT = "on"`). Stages 1–3 are implemented and can be opened with `?rollout=shadow` or `?rollout=canary`. At this course's scale (a few dozen sessions), the canary checks are qualitative. The point is the mechanism: the same code path runs at every stage, and moving between stages is a one-line change.

## Rollback plan

Any of these, from fastest to slowest:

1. **Switch the model off:** set `ROLLOUT = "off"` and push. GitHub Pages republishes in about a minute. The game is then exactly v1 (AE-8 shows this is a tested state).
2. **Go back to the previous model:** set `MODEL_SRC.hfCommit` to the previous pinned commit (kept in the table above) and push. Nothing on Hugging Face has to be deleted.
3. **Revert the release:** `git revert` the v2 commits; the v1 tests still pass.

Rollback triggers: the model fails to load for many players, the support card shows for almost everyone or no one, a regression test fails, or a player reports that the card reveals the answer.

## Trade-off matrix · where should the model run?

| Question | Browser (onnxruntime-web) ✔ chosen | Expo on-device (React Native) | Server (FastAPI on Render) |
|---|---|---|---|
| **Network / latency** | One download (a model under 1 KB + an ~11 MB WASM runtime, cached after the first visit). Inference < 10 ms, works offline after load. | No download at run time, model ships in the app. Fastest, works offline. Needs an app store build to update the model. | Every prediction is a request. Free Render instances sleep, so the first call can take 30–60 s; later calls ~100–300 ms. Fails without network. |
| **Does data leave the device? (KVKK)** | **No.** Features are computed and scored in the browser. | **No.** | **Yes.** Behaviour features go to a third-party host. Needs a legal basis, a privacy notice and a data processing agreement. |
| **Does the model stay secret? (REA risk)** | **No.** Anyone can download `model.onnx` and read the weights (reverse engineering is trivial). | **Mostly no.** The model can be extracted from the app bundle. | **Yes.** Only inputs and outputs are visible; the model can still be approximated by many queries (model extraction). |
| Cost / ops | Free (GitHub Pages + Hugging Face) | Free, but a mobile build pipeline | Free tier with cold starts; one more service to monitor |

**Decision.** The browser wins for this game. The model is not a secret (its weights are in the model card anyway) and it protects nothing valuable, so the REA risk does not matter. Keeping behaviour data on the device is what matters for KVKK, and the browser gives that with no install. The server consumer exists as a bonus and to show that a second runtime gives the same answer (`python tests/parite.py --server <url>`), not as the production path.

## Checklist for this release

- [x] Threshold committed in `spec.md` before training (commit `52a2e8f`)
- [x] `python train.py` passes the gate and writes `model/`
- [x] Python oracle (`tests/parite.py`): onnxruntime vs scikit-learn < 1e-4
- [x] Browser parity (`cypress/e2e/parite.cy.js`): |Δ| < 1e-4 on 5 inputs
- [x] Regression: P1–P8 and AE-1 … AE-5 with `--env rollout=on`
- [x] AE-6, AE-7, AE-8 (`cypress/e2e/model.cy.js`)
- [ ] Model uploaded to Hugging Face, commit pinned in `index.html` and above
- [ ] FastAPI deployed on Render, `parite.py --server` passes

## References

- Amershi, S. et al. (2019). *Software Engineering for Machine Learning: A Case Study.* ICSE-SEIP.
- Shankar, S. et al. (2022). *Operationalizing Machine Learning: An Interview Study.* arXiv:2209.09125.
- Breck, E. et al. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* IEEE Big Data.
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting.* FAT\* 2019.
- Sculley, D. et al. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS.
- Beyer, B. et al. (2016). *Site Reliability Engineering*, ch. "Release Engineering" and canarying. O'Reilly.
