# Project 7: A Gold Set for Extraction

This project measures the extraction pipeline before trusting it at larger
scale. Five real loop-engineering READMEs are hand-labeled in `gold.json`.
`predict.py` runs the same local extraction contract used for the free Project
3 path. `score.py` calculates entity precision, recall, F1, and schema-valid
rate. `ratchet.py` changes one prompt line per attempt and keeps or reverts the
candidate based on the measured score.

The local engine is deterministic so the exercise runs without an API key.
`predict.py --mode opencode` is the real OpenCode adapter; it uses the same
prompt-version and schema contract while leaving the gold set and evaluator
unchanged.

## Run

```bash
python3 ratchet.py
python3 validate.py
```

For a real model experiment, run `python3 ratchet.py opencode` with OpenCode
configured. The deterministic command above is the zero-cost CI gate.

The ratchet runs three attempts and keeps a complete history, including every
reverted candidate. A model output is never accepted based on fluency: its JSON
must validate before its entities count toward the score.

## Metrics

- **Precision:** predicted labels that are in the hand-labeled set.
- **Recall:** hand-labeled labels recovered by the extractor.
- **Schema-valid rate:** valid document outputs divided by all document outputs.

The gold set is intentionally small and human-owned. It is a measuring stick,
not training data to be quietly changed until the prompt wins.
