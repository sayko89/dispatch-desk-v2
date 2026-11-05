# Exam question design · ML in a shipped product

**Learning outcome.** The student can turn a model into a releasable component: state an acceptance criterion before training, test the exported model against an oracle, and plan a release that can be undone.
**Format.** One open question with three parts, 20 points, about 25 minutes, closed book. A one-page excerpt is given with it: a `config.json`, a short `train.py` and a CI log.

---

**Question.** A team adds a model to a quiz app: it predicts whether a student will answer the next question wrongly and, if p ≥ 0.5, shows a hint. Their `train.py` prints `ROC AUC = 0.68`, then exports `model.onnx`. In the browser, the app shows p = 0.4912 for an input where Python gives p = 0.5031. The release went straight to 100 % of users.

a) **(6 pts)** The spec says "ROC AUC ≥ 0.70". List two things wrong with how `train.py` handled this result, and write what it should do instead.

b) **(8 pts)** Is the browser/Python difference a bug? Explain using a tolerance, and say what this difference does to the user. Design a parity test: what is the oracle, what are the inputs, and where does the test run?

c) **(6 pts)** Write a release plan with a rollback in at most 5 lines. Say in one line whether the model should run in the browser or on a server if it reads students' answers, and why.

---

**Model answer and rubric**

| Part | Full marks need | Points |
|---|---|---|
| a | (1) A model below the threshold was exported anyway; the script must **exit non-zero and write no artifact**. (2) The threshold must be committed **before** training, and the metric and split must be fixed (seed, stratified hold-out), otherwise it can be moved after seeing the result. | 3 + 3 |
| b | Yes. |Δ| ≈ 0.012 ≫ 1e-4, so it is a defect, not float noise. It **crosses τ = 0.5**, so the hint appears in Python but not in the app. Oracle = Python (sklearn or onnxruntime) on the same file; inputs = a fixed reference set (e.g. 5 cases, including some near τ) stored as JSON; an E2E test reads the app's displayed p and checks |Δ| < 1e-4. Likely causes: features in a different order, or missing scaling. | 2 + 2 + 3 + 1 |
| c | Shadow (log p, no effect) → canary ~5 % → 25 → 50 → 100 %, each step with a check; rollback = one flag back to "off", or pin the previous model commit. Browser: answers stay on the device (KVKK); the model weights become public, which is acceptable here. A server is also acceptable if the answer mentions sending personal data and the legal basis for it. | 4 + 2 |

**Common wrong answers.** "0.68 is close enough" (zero points for a). "Floating-point error, ignore it" (b loses 4). A rollback that requires retraining (c loses 2).

**Why this question.** It cannot be answered by recalling definitions. The student must read numbers, compare them with a tolerance and a threshold, and connect a test to a user-visible effect. The same three checks are built into this repository: `train.py` (gate), `tests/parite.*` (oracle and parity) and `RELEASE.md` (rollout and rollback).
