---
library_name: sklearn
license: mit
tags:
- onnx
- tabular-classification
- sklearn
- education
- game
pipeline_tag: tabular-classification
---

# Dispatch Desk · costly-decision risk

Predicts, when a crisis scene opens, the probability that this player will pick the costly option, from how they played so far. The game uses it to offer extra support.

## Intended use
- **Use:** inside the Dispatch Desk teaching game, to decide whether to show a support card before a crisis decision.
- **Not for:** grading students, judging real dispatchers, or any decision about a person outside the game.
- **Users:** students playing the game in a browser; the model runs on their device (onnxruntime-web).

## Model
- scikit-learn `Pipeline(StandardScaler -> LogisticRegression)`, seed 13
- Trained with Python 3.13.17, scikit-learn 1.9.1
- Exported to ONNX (opset 17, zipmap off). Input `input` float32 `[n, 8]` in the order below, output `probabilities` `[n, 2]` (column 1 = costly).
- Decision threshold tau = 0.5 (fixed in the spec, not tuned on the test split)

## Features
| name | meaning | example |
|---|---|---|
| `seviye` | Level (0 Just starting, 1 Know a bit, 2 Experienced) | 1.0 |
| `sahne_no` | Crisis number (1-3) | 2.0 |
| `canli_bekleme_ort_dk` | Average call wait in the previous live phase (sim. minutes) | 3.11 |
| `canli_en_yakin_orani` | Share of assignments to the closest crew (0-1) | 0.59 |
| `canli_bekleyen` | Calls still waiting at the alarm | 1.0 |
| `gorev_yanlis` | Field tasks answered wrongly so far | 1.0 |
| `onceki_maliyetli` | Costly choices in earlier crises (0-2) | 0.0 |
| `onceki_karar_suresi_sn` | Seconds spent on the previous crisis (0 for Crisis 1) | 3.7 |

## Coefficients (standardized features)
| feature | weight |
|---|---|
| `seviye` | -0.172 |
| `sahne_no` | -0.136 |
| `canli_bekleme_ort_dk` | +0.628 |
| `canli_en_yakin_orani` | +0.001 |
| `canli_bekleyen` | +0.434 |
| `gorev_yanlis` | +0.636 |
| `onceki_maliyetli` | +0.351 |
| `onceki_karar_suresi_sn` | -0.628 |
| `intercept` | +0.535 |

## Training data
`data/oturumlar.csv` from the GitHub repository: 621 rows, 7 real sessions (21 rows) and 600 synthetic rows from a seeded rule (`data/generate_synthetic.py`, seed 13). No personal data: the session ID is random and no name, location or device field is collected.

## Evaluation (stratified 30 % hold-out, seed 13)
Acceptance gate: ROC AUC >= 0.7 (committed in `spec.md` before training).

| metric | value |
|---|---|
| roc_auc | 0.7876 |
| accuracy | 0.738 |
| f1 | 0.7841 |
| brier | 0.1826 |
| roc_auc_real_only | 0.2 |
| n_test_real | 7 |
| n_rows | 621 |
| n_rows_real | 21 |
| n_sessions_real | 7 |
| positive_rate | 0.5845 |
| onnx_max_abs_diff | 8.44e-08 |

## Limitations and risks
- Most rows are synthetic, so the weights partly reflect the generator's rule. The real-only AUC above is the honest number, and it rests on few sessions.
- Real players were friends of the author, which is a narrow and self-selected group.
- Players who know the model exists could play differently. The model only adds support; it never removes help or changes the outcome.
- The weights are public in this file, so anyone can read them. That is fine here: nothing about the model is secret (see `RELEASE.md`).

## Use
```
https://huggingface.co/<user>/<repo>/resolve/<commit>/model.onnx
```
Always pin a commit, never `main`, so a new upload cannot change a running app.
