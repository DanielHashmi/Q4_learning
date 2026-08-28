#!/usr/bin/env python3
"""Score predictions against the hand-labeled set."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

def score(prediction_path: str = "predictions.json") -> dict:
    gold = json.loads((ROOT / "gold.json").read_text(encoding="utf-8"))
    predictions = json.loads((ROOT / prediction_path).read_text(encoding="utf-8"))
    tp = fp = fn = valid = 0
    for prediction in predictions:
        expected = gold[prediction["document"]]
        try:
            assert isinstance(prediction["entities"], list)
            assert isinstance(prediction["relations"], list)
            assert all("surface_form" in entity and "source" in entity for entity in prediction["entities"])
            valid += 1
        except (AssertionError, KeyError, TypeError):
            continue
        predicted = {entity["surface_form"] for entity in prediction["entities"]}
        actual = set(expected["entities"])
        tp += len(predicted & actual)
        fp += len(predicted - actual)
        fn += len(actual - predicted)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"true_positive":tp,"false_positive":fp,"false_negative":fn,"precision":round(precision,4),"recall":round(recall,4),"f1":round(f1,4),"schema_valid_rate":round(valid / len(predictions),4) if predictions else 0}

if __name__ == "__main__":
    print(json.dumps(score(), indent=2))
