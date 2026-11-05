# Data dictionary · `data/oturumlar.csv`

One row = one crisis decision. A full session has 3 rows (Crisis 1, 2, 3) that share the same `oturum`.

| Column | Type | Values | Meaning | Used by the model |
|---|---|---|---|---|
| `oturum` | text | 8 hex chars | Random session ID made in the browser with `crypto.getRandomValues`. It does not identify a person or a device. | no |
| `surum` | text | `2.0.0`, `synthetic-1` | App version that produced the row (`synthetic-1` = generator) | no |
| `rollout` | text | `off`, `shadow`, `canary`, `on` | Model release stage during the session. Data collection ran with `off`, so the model had no effect on these rows. | no |
| `sahne_no` | int | 1–3 | Crisis number | **yes** |
| `seviye` | int | 0, 1, 2 | Level picked on the intro screen: 0 Just starting, 1 Know a bit, 2 Experienced | **yes** |
| `canli_bekleme_ort_dk` | float | ≥ 0 | Average waiting time (simulated minutes) of the calls in the live phase right before this crisis. A call that was never assigned counts until the alarm. | **yes** |
| `canli_en_yakin_orani` | float | 0–1 | Share of that phase's assignments that went to the closest crew. 0 if nothing was assigned. | **yes** |
| `canli_bekleyen` | int | ≥ 0 | Calls still waiting when the phase's alarm went off | **yes** |
| `gorev_yanlis` | int | 0–5 | Field tasks answered wrongly so far in the session (cumulative) | **yes** |
| `onceki_maliyetli` | int | 0–2 | Costly choices in earlier crises of this session | **yes** |
| `onceki_karar_suresi_sn` | float | ≥ 0 | Real seconds spent on the previous crisis decision (0 for Crisis 1) | **yes** |
| `karar_suresi_sn` | float | ≥ 0 | Real seconds spent on this decision. Known only after the choice, so it is **not** a feature (it would leak the label). | no |
| `secim` | text | `A`, `B` | Option picked | no |
| `sure_doldu` | int | 0, 1 | 1 if the 60 s timer ran out (Experienced level) and the default was applied | no |
| `maliyetli_secim` | int | 0, 1 | **Target.** 1 if the picked option is the costly one: Crisis 1 A, Crisis 2 B, Crisis 3 B. | target |
| `model_p` | float | 0–1 or empty | Model probability shown at the time, empty when the rollout was `off` | no |
| `destek` | int | 0, 1 | 1 if the support card was shown | no |
| `kaynak` | text | `gercek`, `sentetik` | `gercek` = a real person played; `sentetik` = generated. Rows marked `test` (automated `#test` runs) are dropped before training. | filter |

## Where the rows come from

**Real (`gercek`).** Players opened the published game, played normally and, on the end screen, pressed "Copy all sessions on this device" and sent the rows to the author. Nothing is sent to a server. The rows are kept in `data/gercek.csv` exactly as received.

**Synthetic (`sentetik`).** `python data/generate_synthetic.py` (seed 13, 200 sessions) simulates players with a hidden skill `s ~ N(0, 1)`. Skill sets the level they pick (20 % pick a random level), their live-phase play and their thinking time. The label is drawn from:

```
logit = -0.55 + scene offset (C1 +0.30, C2 0, C3 -0.10)
        + 0.35·(wait - 1.2) - 0.90·(closest - 0.6) + 0.25·waiting
        + 0.30·wrong_tasks + 0.45·earlier_costly
        - 0.02·(prev_decision_sec - 20) - 0.35·level + N(0, 0.6)
```

An Experienced player who would take more than 60 s times out, which gives the costly default. The same command always writes the same file, and it writes real rows first and synthetic rows after them.

## Privacy (KVKK)

No name, e-mail, IP, location, device or browser data is collected. The only ID is random and is made fresh for every session. A player can read every value before sending it, because the end screen shows the rows in a text box.
