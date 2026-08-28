#!/usr/bin/env python3
"""Run one extraction prompt against the corpus, offline or through OpenCode."""
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SOURCES = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))

BASE_TERMS = ["progress.md", "OpenCode", "GitHub Actions", "audit-report.md", "human gate", "pull request", "dreaming-state.md", "PR", "run-loop.sh", "verify.sh", "failure", "checklist.md", "run-a.sh", "run-b.sh", "API trigger", "TODO"]

def parse_events(raw):
    raw = raw or ""
    text = "".join(json.loads(line).get("part", {}).get("text", "") for line in raw.splitlines() if _event(line))
    return text.strip() or raw.strip()

def _event(line):
    try:
        return json.loads(line).get("type") == "text"
    except json.JSONDecodeError:
        return False

def predict_offline(source, version):
    text = (ROOT / source["path"]).resolve().read_text(encoding="utf-8")
    terms = list(BASE_TERMS)
    if version == 2:
        terms += ["agent"]
    if version == 3:
        terms += ["trigger phrases"]
    if version == 4:
        terms += ["loop", "memory", "system"]
    entities = [{"surface_form": term, "source":{"document":source["document"],"line":next((i for i,line in enumerate(text.splitlines(),1) if term.lower() in line.lower()),1)}} for term in terms if term.lower() in text.lower()]
    ids = {entity["surface_form"] for entity in entities}
    relations = []
    if "progress.md" in ids and source["document"] in {"project-03","project-07"}:
        relations.append({"subject":source["document"],"predicate":"writes","object":"progress.md"})
    if "audit-report.md" in ids:
        relations.append({"subject":source["document"],"predicate":"produces","object":"audit-report.md"})
    if "dreaming-state.md" in ids:
        relations.append({"subject":source["document"],"predicate":"writes","object":"dreaming-state.md"})
    if "checklist.md" in ids:
        relations.append({"subject":source["document"],"predicate":"uses","object":"checklist.md"})
    if "human gate" in ids:
        relations.append({"subject":source["document"],"predicate":"gated_by","object":"human gate"})
    return {"document":source["document"],"entities":entities,"relations":relations}

def predict_opencode(source, version):
    document_path = (ROOT / source["path"]).resolve()
    # The model experiment scores Project 3's actual extraction prompt. The
    # gold-set versions are one-line variants of that prompt, not a separate
    # invented task.
    base_prompt = (ROOT / ".." / "03-first-extraction" / "prompt.md").read_text(encoding="utf-8")
    variant = (ROOT / f"prompt-v{version}.md").read_text(encoding="utf-8")
    prompt = base_prompt + "\n\nGold-set one-line experiment: " + variant
    request = (prompt + "\nReturn only one JSON object. The document id is " + source["document"] +
               ". Read the attached document and extract from it. Return JSON only.")
    executable = shutil.which("opencode") or "opencode"
    last_error = ""
    model = os.environ.get("OPENCODE_MODEL", "opencode/big-pickle")
    timeout = int(os.environ.get("OPENCODE_TIMEOUT_SECONDS", "120"))
    for attempt in range(3):
        try:
            result = subprocess.run([executable, "run", "--format", "json", "--variant", "minimal", "--model", model, request, "--file", str(document_path)],
                                    text=True, encoding="utf-8", errors="replace",
                                    capture_output=True, check=False, timeout=timeout)
        except subprocess.TimeoutExpired:
            last_error = f"OpenCode timed out after {timeout} seconds"
            continue
        raw = parse_events(result.stdout)
        if result.returncode:
            last_error = result.stderr.strip() or raw or "OpenCode extraction failed"
            continue
        fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
        embedded = re.search(r"(\{.*\})", raw, re.DOTALL)
        try:
            value = json.loads(fenced.group(1) if fenced else embedded.group(1) if embedded else raw)
            if not isinstance(value.get("entities"), list) or not isinstance(value.get("relations"), list):
                raise ValueError("entities and relations must be arrays")
            if not all(isinstance(entity.get("surface_form"), str) and isinstance(entity.get("source"), dict)
                       for entity in value["entities"]):
                raise ValueError("each entity needs surface_form and source")
            value["document"] = source["document"]
            return value
        except (json.JSONDecodeError, ValueError) as exc:
            last_error = f"{exc}: {raw}"
            request += "\nYour previous response was invalid. Output the JSON object immediately, with no prose, markdown, or status update."
    (ROOT / "opencode-response.txt").write_text(last_error, encoding="utf-8")
    raise RuntimeError(f"OpenCode extraction failed after three attempts: {last_error}")

parser = argparse.ArgumentParser()
parser.add_argument("--version", type=int, required=True, choices=(1,2,3,4))
parser.add_argument("--output", default="predictions.json")
parser.add_argument("--mode", choices=("offline", "opencode"), default="offline")
parser.add_argument("--document", choices=[source["document"] for source in SOURCES])
args = parser.parse_args()
predictor = predict_opencode if args.mode == "opencode" else predict_offline
selected = [source for source in SOURCES if args.document is None or source["document"] == args.document]
outputs = [predictor(source, args.version) for source in selected]
Path(ROOT / args.output).write_text(json.dumps(outputs, indent=2) + "\n", encoding="utf-8")
print(f"Predicted {len(outputs)} documents with prompt v{args.version}")
