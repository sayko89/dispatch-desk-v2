"""Build data/oturumlar.csv: the real rows from data/gercek.csv plus seeded synthetic rows.

Rule "synthetic-2" (also documented in data/SOZLUK.md and README.md).
synthetic-1 was too noisy: its own rule reached only ROC AUC 0.72, and its waits and thinking times
did not look like real play (real: ~3.8 sim-min waits, ~3 s decisions). synthetic-2 matches the real ranges
and lowers the noise; see spec.md, decision log.

every synthetic player has a hidden skill s ~ N(0, 1). Skill shapes the level they pick,
how they play the live phases and how long they think. The costly-choice label is drawn from

    logit = -0.40 + scene offset
            + 0.35 * (wait_avg - 3.0) - 0.90 * (closest - 0.6) + 0.25 * waiting
            + 0.30 * wrong_tasks + 0.45 * earlier_costly
            - 0.08 * (prev_decision_sec - 6) - 0.35 * level
            + N(0, 0.3)

Scene offsets: Crisis 1 +0.30 (the cache is tempting), Crisis 2 0, Crisis 3 -0.10.
An Experienced player whose decision takes longer than 60 s times out, which is the costly default.

Seed 13, 200 sessions x 3 crises. Running it twice gives the same file.
Real rows (kaynak=gercek) are copied as they are; rows marked "test" are dropped.
Usage: python data/generate_synthetic.py [--sessions 200] [--seed 13]
"""
import argparse
import csv
import math
import random
from pathlib import Path

COLS = ["oturum", "surum", "rollout", "sahne_no", "seviye", "canli_bekleme_ort_dk", "canli_en_yakin_orani",
        "canli_bekleyen", "gorev_yanlis", "onceki_maliyetli", "onceki_karar_suresi_sn", "karar_suresi_sn",
        "secim", "sure_doldu", "maliyetli_secim", "model_p", "destek", "kaynak"]
COSTLY = {1: "A", 2: "B", 3: "B"}
OTHER = {1: "B", 2: "A", 3: "A"}
TASKS_PER_PHASE = {1: 2, 2: 2, 3: 1}
SCENE_OFFSET = {1: 0.30, 2: 0.0, 3: -0.10}


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def session(rng):
    sid = "%08x" % rng.getrandbits(32)
    s = rng.gauss(0, 1)
    level = 0 if s < -0.6 else (2 if s > 0.7 else 1)
    if rng.random() < 0.2:  # some players misjudge their level
        level = rng.choice([0, 1, 2])
    wrong, costly_so_far, prev_sec, rows = 0, 0, 0.0, []
    for no in (1, 2, 3):
        wait = clip(rng.lognormvariate(math.log(3.0) - 0.35 * s, 0.45), 0.1, 10)
        closest = clip(0.6 + 0.15 * s + rng.gauss(0, 0.15), 0, 1)
        waiting = min(5, sum(rng.random() < sigmoid(-1.2 - 0.9 * s) for _ in range(4)))
        wrong += sum(rng.random() < sigmoid(-0.3 - 0.8 * s) for _ in range(TASKS_PER_PHASE[no]))
        sec = clip(rng.lognormvariate(math.log(6) + 0.25 * s, 0.6), 1, 120)
        logit = (-0.40 + SCENE_OFFSET[no] + 0.35 * (wait - 3.0) - 0.90 * (closest - 0.6) + 0.25 * waiting
                 + 0.30 * wrong + 0.45 * costly_so_far - 0.08 * (prev_sec - 6) - 0.35 * level + rng.gauss(0, 0.3))
        timed_out = level == 2 and sec > 60
        if timed_out:
            sec, costly = 60.0, 1
        else:
            costly = int(rng.random() < sigmoid(logit))
        rows.append({
            "oturum": sid, "surum": "synthetic-2", "rollout": "off", "sahne_no": no, "seviye": level,
            "canli_bekleme_ort_dk": round(wait, 2), "canli_en_yakin_orani": round(closest, 2),
            "canli_bekleyen": waiting, "gorev_yanlis": wrong, "onceki_maliyetli": costly_so_far,
            "onceki_karar_suresi_sn": round(prev_sec, 1), "karar_suresi_sn": round(sec, 1),
            "secim": COSTLY[no] if costly else OTHER[no], "sure_doldu": int(timed_out),
            "maliyetli_secim": costly, "model_p": "", "destek": 0, "kaynak": "sentetik",
        })
        costly_so_far += costly
        prev_sec = sec
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", type=int, default=200)
    ap.add_argument("--seed", type=int, default=13)
    here = Path(__file__).parent
    ap.add_argument("--real", default=str(here / "gercek.csv"))
    ap.add_argument("--out", default=str(here / "oturumlar.csv"))
    a = ap.parse_args()
    rng = random.Random(a.seed)
    real = []
    if Path(a.real).exists():
        with open(a.real, newline="") as f:
            seen = set()
            for r in csv.DictReader(f):
                key = (r.get("oturum"), r.get("sahne_no"))  # "copy all" repeats earlier sessions: keep one copy
                if r.get("kaynak") == "gercek" and key not in seen:
                    seen.add(key)
                    real.append({c: r.get(c, "") for c in COLS})
    synth = [r for _ in range(a.sessions) for r in session(rng)]
    rows = real + synth
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    n_real = len({r["oturum"] for r in real})
    pos = sum(int(r["maliyetli_secim"]) for r in rows) / len(rows)
    print(f"{len(real)} real rows ({n_real} sessions) + {len(synth)} synthetic rows -> {a.out} (positive rate {pos:.2f})")


if __name__ == "__main__":
    main()
