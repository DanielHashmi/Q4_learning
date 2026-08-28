#!/usr/bin/env python3
"""Build a 20-form resolution corpus from Project 3 output plus real aliases."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
P3 = ROOT.parent / "03-first-extraction" / "output"
forms = []
for path in sorted(P3.glob("project-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    forms.extend({
        "surface_form": entity["surface_form"],
        "type": entity["type"],
        "description": entity["description"],
        "source": entity["source"],
    } for entity in data["entities"])

# These are additional surface forms present in the same three READMEs but not
# required by the small first extractor's ontology.
forms.extend([
    {"surface_form":"morning brief","type":"PROJECT","description":"The scheduled TODO brief loop.","source":{"document":"project-03-morning-brief","line":1}},
    {"surface_form":"daily loop","type":"PROCESS","description":"The unattended daily dependency audit loop.","source":{"document":"project-08-daily-loop","line":1}},
    {"surface_form":"dreaming loop","type":"PROCESS","description":"The weekly improvement pass over prior loop evidence.","source":{"document":"project-12-dreaming-loop","line":1}},
    {"surface_form":"PR","type":"ARTIFACT","description":"A GitHub pull request containing a proposed change.","source":{"document":"project-08-daily-loop","line":7}},
    {"surface_form":"pull request","type":"ARTIFACT","description":"A GitHub pull request containing a proposed change.","source":{"document":"project-08-daily-loop","line":7}},
])

# Keep a pre-trap snapshot so the required two-pass experiment is reproducible.
Path(ROOT / "surface_forms_before_trap.json").write_text(json.dumps(forms, indent=2) + "\n", encoding="utf-8")

# Same name, different things: this is the trap the resolver must not merge.
forms.extend([
    {"surface_form":"review","type":"PROCESS","description":"Automated read-only review of a proposed code change.","source":{"document":"project-08-daily-loop","line":7}},
    {"surface_form":"review","type":"GATE","description":"Human decision to inspect and merge a pull request.","source":{"document":"project-08-daily-loop","line":15}},
])

Path(ROOT / "surface_forms.json").write_text(json.dumps(forms, indent=2) + "\n", encoding="utf-8")
print(f"Prepared {len(forms)} surface forms")
