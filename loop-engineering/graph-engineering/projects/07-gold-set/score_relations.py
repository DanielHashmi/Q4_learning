#!/usr/bin/env python3
"""Score extracted relation triples against the Project 7 hand labels."""
import json
from pathlib import Path
ROOT = Path(__file__).parent
gold = json.loads((ROOT / "gold.json").read_text(encoding="utf-8"))
predictions = json.loads((ROOT / "predictions.json").read_text(encoding="utf-8"))
tp = fp = fn = 0
for prediction in predictions:
    expected = {tuple(item) for item in gold[prediction["document"]]["relations"]}
    actual = {(item["subject"], item["predicate"], item["object"]) for item in prediction["relations"]}
    tp += len(actual & expected); fp += len(actual - expected); fn += len(expected - actual)
precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
print(json.dumps({"true_positive":tp,"false_positive":fp,"false_negative":fn,"precision":round(precision,4),"recall":round(recall,4),"f1":round(f1,4)}, indent=2))
