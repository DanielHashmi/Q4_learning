#!/usr/bin/env python3
"""Run Project 3 extraction with a deterministic free path or OpenCode.

The offline path is intentionally explicit rather than pretending to be an LLM:
it extracts a small ontology using rules and produces the exact same contract
that a headless model run must satisfy.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SOURCES = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
PROMPT = (ROOT / "prompt.md").read_text(encoding="utf-8")
OUTPUT = ROOT / "output"


def line_for(lines: list[str], phrase: str) -> int:
    for number, line in enumerate(lines, 1):
        if phrase.lower() in line.lower():
            return number
    return 1


def stable_id(kind: str, value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return f"{kind.lower()}_{value}"


def offline_extract(source: dict, text: str) -> dict:
    lines = text.splitlines()
    entities: list[dict] = []
    relations: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(kind: str, surface: str, description: str, line: int | None = None) -> str:
        key = (kind, surface)
        identifier = stable_id(kind, surface)
        if key not in seen:
            entities.append({
                "id": identifier,
                "type": kind,
                "surface_form": surface,
                "description": description,
                "source": {"document": source["document"], "line": line or line_for(lines, surface)},
            })
            seen.add(key)
        return identifier

    heading = next((line.lstrip("# ") for line in lines if line.startswith("# Project ")), source["document"])
    project = add("PROJECT", heading, "A loop-engineering project described by this README.", line_for(lines, heading))

    terms = [
        ("ARTIFACT", "progress.md", "Committed spine file carrying state between fresh runs."),
        ("ARTIFACT", "audit-report.md", "Dependency audit output produced by the daily loop."),
        ("ARTIFACT", "dreaming-state.md", "Cursor and state for the improvement loop."),
        ("TOOL", "OpenCode", "Headless coding-agent CLI used by the automation."),
        ("TOOL", "OpenCode CLI", "Headless coding-agent command described by the project."),
        ("PROCESS", "spine", "Durable state read before a beat and written after it."),
        ("PROCESS", "committed spine", "A spine persisted in Git for the next fresh runner."),
        ("GATE", "human gate", "A human decision required before risky work is merged."),
        ("GATE", "human review and merge", "Human review and merge action at the end of a PR loop."),
        ("TOOL", "GitHub Actions", "Hosted automation runner that starts scheduled or event-driven beats."),
    ]
    term_ids: dict[str, str] = {}
    for kind, surface, description in terms:
        if any(surface.lower() in line.lower() for line in lines):
            term_ids[surface] = add(kind, surface, description)

    def relation(subject: str, predicate: str, object_id: str, phrase: str) -> None:
        relations.append({
            "subject": subject,
            "predicate": predicate,
            "object": object_id,
            "source": {"document": source["document"], "line": line_for(lines, phrase)},
        })

    if "progress.md" in term_ids:
        relation(project, "writes", term_ids["progress.md"], "progress.md")
    if "audit-report.md" in term_ids:
        relation(project, "produces", term_ids["audit-report.md"], "audit-report.md")
    if "dreaming-state.md" in term_ids:
        relation(project, "writes", term_ids["dreaming-state.md"], "dreaming-state.md")
    if "OpenCode" in term_ids:
        relation(project, "uses", term_ids["OpenCode"], "OpenCode")
    if "OpenCode CLI" in term_ids:
        relation(project, "uses", term_ids["OpenCode CLI"], "OpenCode CLI")
    if "human gate" in term_ids:
        relation(project, "gated_by", term_ids["human gate"], "human gate")
    if "human review and merge" in term_ids:
        relation(project, "gated_by", term_ids["human review and merge"], "human review and merge")
    if "GitHub Actions" in term_ids:
        relation(project, "uses", term_ids["GitHub Actions"], "GitHub Actions")
    return {"document": source["document"], "entities": entities, "relations": relations}


def validate_shape(result: dict, expected_document: str) -> None:
    if result.get("document") != expected_document:
        raise ValueError(f"document mismatch: expected {expected_document!r}")
    if not isinstance(result.get("entities"), list) or not isinstance(result.get("relations"), list):
        raise ValueError("entities and relations must be arrays")
    entity_ids = {entity.get("id") for entity in result["entities"]}
    if None in entity_ids or len(entity_ids) != len(result["entities"]):
        raise ValueError("entity IDs must be present and unique")
    for entity in result["entities"]:
        if entity.get("type") not in {"PROJECT", "ARTIFACT", "TOOL", "PROCESS", "GATE", "MEMORY"}:
            raise ValueError(f"invalid entity type: {entity}")
        source = entity.get("source", {})
        if source.get("document") != expected_document or not isinstance(source.get("line"), int) or source["line"] < 1:
            raise ValueError(f"invalid entity source: {entity}")
    for relation in result["relations"]:
        if relation.get("subject") not in entity_ids or relation.get("object") not in entity_ids:
            raise ValueError(f"relation endpoint missing: {relation}")
        if relation.get("predicate") not in {"reads", "writes", "uses", "requires", "produces", "gated_by", "runs", "contains"}:
            raise ValueError(f"invalid predicate: {relation}")
        source = relation.get("source", {})
        if source.get("document") != expected_document or not isinstance(source.get("line"), int) or source["line"] < 1:
            raise ValueError(f"invalid relation source: {relation}")


def opencode_extract(source: dict, text: str) -> dict:
    document_path = (ROOT / source["path"]).resolve()
    request = (f"{PROMPT}\n\nDocument identifier: {source['document']}\n"
               "Read the attached document and extract from it. Return only the JSON object.")
    for attempt in range(2):
        completed = subprocess.run(
            [shutil.which("opencode") or "opencode", "run", "--format", "json", "--variant", "minimal", "--model", "opencode/big-pickle", request, "--file", str(document_path)],
            text=True, capture_output=True, check=False, timeout=240,
        )
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip() or "OpenCode extraction failed")
        text_parts = []
        for line in completed.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "text":
                text_parts.append(event.get("part", {}).get("text", ""))
        raw = "".join(text_parts).strip() or completed.stdout.strip()
        fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
        if fenced:
            raw = fenced.group(1)
        try:
            candidate = json.loads(raw)
            validate_shape(candidate, source["document"])
            return candidate
        except (json.JSONDecodeError, ValueError) as exc:
            if attempt == 1:
                raise ValueError(f"OpenCode returned schema-invalid JSON: {exc}") from exc
            request = (f"Previous output failed schema validation: {exc}. Return only JSON. "
                       "Types must be exactly PROJECT, ARTIFACT, TOOL, PROCESS, GATE, or MEMORY. "
                       "Read the attached document again. " + request)
    raise AssertionError("unreachable")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("offline", "opencode"), default="offline")
    args = parser.parse_args()
    OUTPUT.mkdir(exist_ok=True)
    duplicate_surface_forms: dict[str, list[dict]] = {}
    for source in SOURCES:
        path = (ROOT / source["path"]).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        result = offline_extract(source, text) if args.mode == "offline" else opencode_extract(source, text)
        # The runner owns document identity; this prevents a model paraphrase from\n        # attributing valid extracted records to the wrong input document.\n        result["document"] = source["document"]\n        validate_shape(result, source["document"])
        (OUTPUT / f"{source['document']}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        for entity in result["entities"]:
            key = entity["type"] + ":" + entity["description"]
            duplicate_surface_forms.setdefault(key, []).append({"document": source["document"], "surface_form": entity["surface_form"], "id": entity["id"]})
    duplicates = [
        {"concept": key, "surface_forms": values}
        for key, values in duplicate_surface_forms.items()
        if len({value["surface_form"].lower() for value in values}) > 1
    ]
    (OUTPUT / "duplicates.json").write_text(json.dumps(duplicates, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(SOURCES)} documents in {args.mode} mode")
    print(f"Duplicate concepts with multiple surface forms: {len(duplicates)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"Extraction failed: {exc}", file=sys.stderr)
        raise SystemExit(1)




