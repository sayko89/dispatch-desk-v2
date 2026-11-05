"""Python oracle for the parity tests.

    python tests/parite.py            # (re)write tests/parite.json from model/model.onnx
    python tests/parite.py --check    # check parite.json against the current model
    python tests/parite.py --server https://<app>.onrender.com   # check the FastAPI consumer too

The oracle runs the same model.onnx with Python onnxruntime and, independently, recomputes p
with scikit-learn retrained by train.py's exact recipe. Both must agree within 1e-4.
The browser test (cypress/e2e/parite.cy.js) then checks the app's data-cy="p" against these values.
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
OUT = ROOT / "tests" / "parite.json"
TOL = 1e-4

# Five reference inputs: two from the acceptance examples, three around the decision threshold.
CASES = [
    ("AE-6 struggling player, Crisis 3",
     dict(seviye=0, sahne_no=3, canli_bekleme_ort_dk=3.5, canli_en_yakin_orani=0, canli_bekleyen=4, gorev_yanlis=5, onceki_maliyetli=2, onceki_karar_suresi_sn=4)),
    ("AE-7 steady player, Crisis 3",
     dict(seviye=2, sahne_no=3, canli_bekleme_ort_dk=0.3, canli_en_yakin_orani=1, canli_bekleyen=0, gorev_yanlis=0, onceki_maliyetli=0, onceki_karar_suresi_sn=25)),
    ("Typical player, Crisis 1",
     dict(seviye=1, sahne_no=1, canli_bekleme_ort_dk=1.2, canli_en_yakin_orani=0.6, canli_bekleyen=1, gorev_yanlis=1, onceki_maliyetli=0, onceki_karar_suresi_sn=0)),
    ("New player, quick and careful, Crisis 2",
     dict(seviye=0, sahne_no=2, canli_bekleme_ort_dk=0.8, canli_en_yakin_orani=0.9, canli_bekleyen=0, gorev_yanlis=0, onceki_maliyetli=1, onceki_karar_suresi_sn=40)),
    ("Experienced but rushed, Crisis 2",
     dict(seviye=2, sahne_no=2, canli_bekleme_ort_dk=2.4, canli_en_yakin_orani=0.4, canli_bekleyen=2, gorev_yanlis=3, onceki_maliyetli=1, onceki_karar_suresi_sn=3.5)),
]


def onnx_p(names, rows):
    sess = ort.InferenceSession(str(MODEL / "model.onnx"))
    x = np.array([[r[n] for n in names] for r in rows], dtype=np.float32)
    return sess.run(["probabilities"], {"input": x})[0][:, 1]


def sklearn_p(names, rows):
    sys.path.insert(0, str(ROOT))
    import pandas as pd
    import train
    from sklearn.model_selection import train_test_split
    df = pd.read_csv(train.DATA)
    df = df[df["kaynak"].isin(["gercek", "sentetik"])].reset_index(drop=True)
    X, y = df[names].astype(float), df[train.TARGET].astype(int)
    X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.3, stratify=y, random_state=train.SEED)
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=train.SEED)).fit(X_tr, y_tr)
    return m.predict_proba(pd.DataFrame(rows, columns=names).astype(float))[:, 1]


def server_p(url, rows):
    out = []
    for r in rows:
        req = urllib.request.Request(url.rstrip("/") + "/predict", data=json.dumps(r).encode(), headers={"Content-Type": "application/json"})
        out.append(json.load(urllib.request.urlopen(req, timeout=60))["p"])
    return np.array(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--server")
    a = ap.parse_args()
    cfg = json.loads((MODEL / "config.json").read_text(encoding="utf-8"))
    names = [f["name"] for f in cfg["features"]]
    rows = [c for _, c in CASES]
    p_onnx, p_sk = onnx_p(names, rows), sklearn_p(names, rows)
    worst = float(np.abs(p_onnx - p_sk).max())
    print(f"onnxruntime vs scikit-learn: max |diff| {worst:.2e}")
    ok = worst < TOL
    if a.check or a.server:
        ref = json.loads(OUT.read_text(encoding="utf-8"))
        d = float(np.abs(np.array([c["p"] for c in ref["cases"]]) - p_onnx).max())
        print(f"parite.json vs current model: max |diff| {d:.2e}")
        ok &= d < TOL
    else:
        OUT.write_text(json.dumps({
            "model_version": cfg["version"], "tolerance": TOL, "decision_threshold": cfg["decision_threshold"],
            "features": names,
            "cases": [{"name": n, "input": c, "p": round(float(p), 8), "support": bool(p >= cfg["decision_threshold"])}
                      for (n, c), p in zip(CASES, p_onnx)],
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    if a.server:
        p_srv = server_p(a.server, rows)
        d = float(np.abs(p_srv - p_onnx).max())
        print(f"server vs oracle: max |diff| {d:.2e}")
        ok &= d < TOL
    for (n, _), p in zip(CASES, p_onnx):
        print(f"  {p:.6f}  {n}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
