#!/usr/bin/env python3
"""Resolve surface forms into reversible canonical clusters."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

def parse_opencode_events(raw: str) -> str:
    parts = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "text":
            parts.append(event.get("part", {}).get("text", ""))
    return "".join(parts).strip() or raw.strip()

def opencode(forms: list[dict], input_path: Path) -> dict:
    executable = shutil.which("opencode") or "opencode"
    request = (f"Use your file-reading tool to read the attached {input_path.name}. "
               "It is an indexed array of entity mentions. Return only JSON in this exact shape: "
               "{\"clusters\":[{\"canonical_id\":\"id\",\"type\":\"TYPE\","
               "\"aliases\":[0],\"rationale\":\"why\",\"confidence\":0.0}]}. "
               "Every integer index must occur exactly once. Merge only mentions that name the same "
               "real entity. Keep the two review mentions separate because their type and role differ.")
    for attempt in range(2):
        completed = subprocess.run(
            [executable, "run", "--format", "json", "--variant", "minimal", "--model", "opencode/big-pickle",
             request, "--file", str(input_path)],
            text=True, capture_output=True, check=False, timeout=240,
        )
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip() or "OpenCode resolution failed")
        raw = parse_opencode_events(completed.stdout)
        fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
        try:
            result = json.loads(fenced.group(1) if fenced else raw)
            aliases = [alias for cluster in result["clusters"] for alias in cluster["aliases"]]
            if sorted(aliases) != list(range(len(forms))):
                raise ValueError("each input index must occur exactly once")
            if any(not cluster.get("canonical_id") or not cluster.get("rationale") or
                   not isinstance(cluster.get("confidence"), (int, float)) or not 0 <= cluster["confidence"] <= 1
                   for cluster in result["clusters"]):
                raise ValueError("each cluster needs id, rationale, and confidence")
            return {"schema_version": "1.0", "clusters": result["clusters"]}
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            if attempt == 1:
                (ROOT / "opencode-response.txt").write_text(raw, encoding="utf-8")
                raise ValueError(f"OpenCode resolution returned schema-invalid clusters: {exc}") from exc
            request = (f"Your previous response failed validation: {exc}. "
                       "Retry with only the exact JSON object and include every integer alias once.\n" + request)
    raise AssertionError("unreachable")

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")

def offline(forms: list[dict]) -> dict:
    clusters: list[dict] = []
    consumed: set[int] = set()

    explicit = [
        ("memory_spine", {"progress.md", "spine", "committed spine"}, "These forms name durable state carried between fresh runs.", 0.98),
        ("opencode", {"OpenCode", "OpenCode CLI"}, "The CLI and its short product name refer to the same headless tool.", 0.98),
        ("pull_request", {"PR", "pull request"}, "Both forms name the same GitHub review artifact.", 0.99),
    ]
    for canonical, aliases, rationale, confidence in explicit:
        members = [index for index, form in enumerate(forms) if form["surface_form"] in aliases]
        if members:
            consumed.update(members)
            clusters.append({"canonical_id": canonical, "type": forms[members[0]]["type"], "aliases": [forms[i] for i in members], "rationale": rationale, "confidence": confidence})

    for index, form in enumerate(forms):
        if index in consumed:
            continue
        same = [j for j, other in enumerate(forms) if j not in consumed and other["surface_form"].lower() == form["surface_form"].lower() and other["type"] == form["type"] and other["description"] == form["description"]]
        if not same:
            same = [index]
        consumed.update(same)
        clusters.append({"canonical_id": f"mention_{index:03d}_{slug(form['surface_form'])}", "type": form["type"], "aliases": [forms[i] for i in same], "rationale": "No stronger evidence supports merging this surface form with another canonical entity.", "confidence": 0.7 if len(same) == 1 else 0.93})

    return {"schema_version":"1.0", "clusters":clusters}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("offline", "opencode"), default="offline")
    parser.add_argument("--input", type=Path, default=ROOT / "surface_forms.json")
    parser.add_argument("--output", type=Path, default=ROOT / "resolved.json")
    args = parser.parse_args()
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    forms = json.loads(input_path.read_text(encoding="utf-8"))
    result = offline(forms) if args.mode == "offline" else opencode(forms, input_path)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Resolved {len(forms)} surface forms into {len(result['clusters'])} canonical clusters")

if __name__ == "__main__":
    main()
