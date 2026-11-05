"""Server consumer of the Dispatch Desk v2 model (bonus).

    uvicorn server.app:app --reload            # local, uses model/ from this repo
    MODEL_BASE=https://huggingface.co/saiyko/dispatch-desk-risk/resolve/<commit>/ uvicorn server.app:app

POST /predict with the 8 features as JSON -> {"p": ..., "support": ..., "model_version": ...}
The result must match tests/parite.json within 1e-4: python tests/parite.py --server <url>
"""
import json
import os
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("MODEL_BASE", "").strip()


def _load(name):
    if BASE:
        with urllib.request.urlopen(BASE.rstrip("/") + "/" + name, timeout=60) as r:
            return r.read()
    return (ROOT / "model" / name).read_bytes()


CONFIG = json.loads(_load("config.json"))
SESSION = ort.InferenceSession(_load("model.onnx"), providers=["CPUExecutionProvider"])
NAMES = [f["name"] for f in CONFIG["features"]]
TAU = CONFIG["decision_threshold"]


class Features(BaseModel):
    seviye: float = Field(ge=0, le=2)
    sahne_no: float = Field(ge=1, le=3)
    canli_bekleme_ort_dk: float = Field(ge=0)
    canli_en_yakin_orani: float = Field(ge=0, le=1)
    canli_bekleyen: float = Field(ge=0)
    gorev_yanlis: float = Field(ge=0)
    onceki_maliyetli: float = Field(ge=0, le=2)
    onceki_karar_suresi_sn: float = Field(ge=0)


app = FastAPI(title="Dispatch Desk v2 · risk model", version=CONFIG["version"])
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"ok": True, "model_version": CONFIG["version"], "source": BASE or "bundled model/", "features": NAMES,
            "roc_auc": CONFIG["metrics"]["roc_auc"]}


@app.post("/predict")
def predict(f: Features):
    x = np.array([[getattr(f, n) for n in NAMES]], dtype=np.float32)
    try:
        p = float(SESSION.run(["probabilities"], {"input": x})[0][0, 1])
    except Exception as e:  # pragma: no cover
        raise HTTPException(500, str(e))
    return {"p": p, "support": p >= TAU, "threshold": TAU, "model_version": CONFIG["version"]}
