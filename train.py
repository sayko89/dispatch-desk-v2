"""Train the Dispatch Desk v2 costly-decision risk model.

    python train.py            # reads data/oturumlar.csv, writes model/

Contract (spec.md, section 11):
- fixed seed 13, stratified 70/30 split, StandardScaler -> LogisticRegression
- primary metric ROC AUC on the test split, acceptance threshold 0.70
- ONNX probabilities must match scikit-learn within 1e-4
- if either check fails: exit code 1 and no model files are left in model/
"""
import json
import platform
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "oturumlar.csv"
MODEL_DIR = ROOT / "model"
SEED = 13
AUC_THRESHOLD = 0.70  # committed in spec.md before the first training run
DECISION_THRESHOLD = 0.50  # tau: p >= tau -> support card
PARITY_TOL = 1e-4
TARGET = "maliyetli_secim"
FEATURES = [
    ("seviye", "Level (0 Just starting, 1 Know a bit, 2 Experienced)"),
    ("sahne_no", "Crisis number (1-3)"),
    ("canli_bekleme_ort_dk", "Average call wait in the previous live phase (sim. minutes)"),
    ("canli_en_yakin_orani", "Share of assignments to the closest crew (0-1)"),
    ("canli_bekleyen", "Calls still waiting at the alarm"),
    ("gorev_yanlis", "Field tasks answered wrongly so far"),
    ("onceki_maliyetli", "Costly choices in earlier crises (0-2)"),
    ("onceki_karar_suresi_sn", "Seconds spent on the previous crisis (0 for Crisis 1)"),
]
NAMES = [n for n, _ in FEATURES]
OUT_FILES = ("model.onnx", "config.json", "README.md")


def fail(msg):
    for name in OUT_FILES:  # never leave a model behind that did not pass the gate
        (MODEL_DIR / name).unlink(missing_ok=True)
    sys.exit(f"FAIL: {msg}. No model was written.")


def export_onnx(model, X, path):
    import onnxruntime as ort
    from skl2onnx import to_onnx
    from skl2onnx.common.data_types import FloatTensorType

    onx = to_onnx(model, initial_types=[("input", FloatTensorType([None, X.shape[1]]))],
                  options={id(model): {"zipmap": False}}, target_opset=17)
    path.write_bytes(onx.SerializeToString())
    sess = ort.InferenceSession(str(path))
    p_onnx = sess.run(["probabilities"], {"input": X.to_numpy(np.float32)})[0]
    return float(np.abs(p_onnx - model.predict_proba(X)).max())


def model_card(cfg):
    m = cfg["metrics"]
    rows = "\n".join(f"| {k} | {v} |" for k, v in m.items())
    feats = "\n".join(f"| `{f['name']}` | {f['label']} | {f['example']} |" for f in cfg["features"])
    coefs = "\n".join(f"| `{k}` | {v:+.3f} |" for k, v in cfg["coefficients"].items())
    return f"""---
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

# {cfg["title"]}

{cfg["description"]}

## Intended use
- **Use:** inside the Dispatch Desk teaching game, to decide whether to show a support card before a crisis decision.
- **Not for:** grading students, judging real dispatchers, or any decision about a person outside the game.
- **Users:** students playing the game in a browser; the model runs on their device (onnxruntime-web).

## Model
- scikit-learn `Pipeline(StandardScaler -> LogisticRegression)`, seed {cfg["seed"]}
- Trained with Python {cfg["python_version"]}, scikit-learn {cfg["sklearn_version"]}
- Exported to ONNX (opset 17, zipmap off). Input `input` float32 `[n, {len(cfg["features"])}]` in the order below, output `probabilities` `[n, 2]` (column 1 = costly).
- Decision threshold tau = {cfg["decision_threshold"]} (fixed in the spec, not tuned on the test split)

## Features
| name | meaning | example |
|---|---|---|
{feats}

## Coefficients (standardized features)
| feature | weight |
|---|---|
{coefs}

## Training data
`data/oturumlar.csv` from the GitHub repository: {m["n_rows"]} rows, {m["n_sessions_real"]} real sessions ({m["n_rows_real"]} rows) and {m["n_rows"] - m["n_rows_real"]} synthetic rows from a seeded rule (`data/generate_synthetic.py`, seed 13). No personal data: the session ID is random and no name, location or device field is collected.

## Evaluation (stratified 30 % hold-out, seed {cfg["seed"]})
Acceptance gate: ROC AUC >= {cfg["acceptance"]["roc_auc_min"]} (committed in `spec.md` before training).

| metric | value |
|---|---|
{rows}

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
"""


def main():
    df = pd.read_csv(DATA)
    df = df[df["kaynak"].isin(["gercek", "sentetik"])].reset_index(drop=True)
    X, y = df[NAMES].astype(float), df[TARGET].astype(int)
    X_tr, X_te, y_tr, y_te, k_tr, k_te = train_test_split(
        X, y, df["kaynak"], test_size=0.3, stratify=y, random_state=SEED)

    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=SEED))
    model.fit(X_tr, y_tr)
    p = model.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_te, p)
    real = (k_te == "gercek").to_numpy()
    real_auc = roc_auc_score(y_te[real], p[real]) if real.sum() and y_te[real].nunique() == 2 else None
    pred = (p >= DECISION_THRESHOLD).astype(int)
    metrics = {
        "roc_auc": round(float(auc), 4),
        "accuracy": round(float(accuracy_score(y_te, pred)), 4),
        "f1": round(float(f1_score(y_te, pred)), 4),
        "brier": round(float(brier_score_loss(y_te, p)), 4),
        "roc_auc_real_only": None if real_auc is None else round(float(real_auc), 4),
        "n_test_real": int(real.sum()),
        "n_rows": int(len(df)),
        "n_rows_real": int((df["kaynak"] == "gercek").sum()),
        "n_sessions_real": int(df.loc[df["kaynak"] == "gercek", "oturum"].nunique()),
        "positive_rate": round(float(y.mean()), 4),
    }
    print(json.dumps(metrics, indent=2))
    if auc < AUC_THRESHOLD:
        fail(f"ROC AUC {auc:.4f} is below the acceptance threshold {AUC_THRESHOLD}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        diff = export_onnx(model, X_te, tmp / "model.onnx")
        metrics["onnx_max_abs_diff"] = float(f"{diff:.2e}")
        if diff > PARITY_TOL:
            fail(f"ONNX differs from scikit-learn by {diff:.2e} (> {PARITY_TOL})")
        lr = model[-1]
        cfg = {
            "title": "Dispatch Desk · costly-decision risk",
            "description": "Predicts, when a crisis scene opens, the probability that this player will pick the costly option, from how they played so far. The game uses it to offer extra support.",
            "version": "2.0.0",
            "target": TARGET,
            "classes": [0, 1],
            "class_labels": ["not costly", "costly"],
            "features": [{"name": n, "label": l, "example": float(X[n].median())} for n, l in FEATURES],
            "decision_threshold": DECISION_THRESHOLD,
            "acceptance": {"metric": "roc_auc", "roc_auc_min": AUC_THRESHOLD, "split": "stratified 70/30", "parity_tol": PARITY_TOL},
            "coefficients": {n: round(float(c), 4) for n, c in zip(NAMES, lr.coef_[0])} | {"intercept": round(float(lr.intercept_[0]), 4)},
            "metrics": metrics,
            "seed": SEED,
            "sklearn_version": sklearn.__version__,
            "python_version": platform.python_version(),
        }
        (tmp / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (tmp / "README.md").write_text(model_card(cfg), encoding="utf-8")
        MODEL_DIR.mkdir(exist_ok=True)
        for name in OUT_FILES:
            shutil.copyfile(tmp / name, MODEL_DIR / name)
    print(f"PASS: ROC AUC {auc:.4f} >= {AUC_THRESHOLD}, ONNX diff {diff:.1e}. Wrote model/{{{','.join(OUT_FILES)}}}")


if __name__ == "__main__":
    main()
