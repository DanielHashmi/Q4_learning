# Graph Engineering Projects

A practical progression for turning agent activity into a **queryable, evidence-backed graph**: model systems, preserve provenance, extract structured records, resolve identities, ground review, measure quality, and connect memory across loops.

## Project map

| Project | Focus | What it demonstrates |
| --- | --- | --- |
| [01 · Draw Your Real System](./01-draw-system/) | Graph modeling | Real loops, files, gates, and anchors become typed nodes and labeled directed edges. |
| [02 · Spine to Claims](./02-spine-to-claims/) | Provenance | Durable findings become typed claims with sources, confidence, and explicit inference status. |
| [03 · First Extraction](./03-first-extraction/) | Structured extraction | Project READMEs are converted into schema-constrained records while surface forms remain traceable. |
| [04 · The DAG Speaks](./04-dag-speaks/) | Git lineage | Tested Git queries reveal descendants, unexplored frontier tips, and commit paths without transcript parsing. |
| [05 · Resolution Drill](./05-resolution-drill/) | Entity resolution | Genuine aliases are merged while ambiguous same-name entities remain separate. |
| [06 · Grounded Reviewer](./06-grounded-reviewer/) | Evidence-backed review | Factual statements must cite active graph claims; unsupported or inference-only claims receive `REVISE`. |
| [07 · Gold Set](./07-gold-set/) | Measurement | A human-owned gold set measures precision, recall, F1, and schema validity across prompt iterations. |
| [08 · Capstone](./08-capstone/) | Graph memory | Separate triage and changelog loops share append-only claims, run records, and captured Git evidence. |

## The progression

```text
model → provenance → extract → traverse → resolve → ground → measure → connect
```

The projects separate concerns that are easy to blur together: **extraction** records what was written, **resolution** decides which mentions refer to the same entity, **provenance** preserves why a claim exists, and **grounded review** checks whether a statement is supported. The capstone combines these ideas into inspectable graph memory shared across separate workspaces.

## Design principles

The graph is intentionally stored in ordinary files such as JSON and Mermaid so it remains inspectable, versionable, and testable. Validators reject malformed structure, missing provenance, invalid references, and unauthorized mutations before results are trusted. A fluent model response is never treated as evidence by itself.

## Start here

Read the projects in numerical order for the intended progression. Begin with [01 · Draw Your Real System](./01-draw-system/) to learn the node-and-edge model, then follow [03 · First Extraction](./03-first-extraction/) and [05 · Resolution Drill](./05-resolution-drill/) to see why extraction and identity resolution remain separate. Finish with [08 · Capstone](./08-capstone/) for the two-loop, one-graph design.

> These projects are educational experiments. Review each project’s README for local runtime requirements, optional provider credentials, and the exact validation command before running it.
