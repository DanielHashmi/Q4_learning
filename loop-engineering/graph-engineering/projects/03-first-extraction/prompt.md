# Extraction contract

Read the supplied document and return **only** one JSON object with this shape:

```json
{
  "document": "relative/path.md",
  "entities": [
    {
      "id": "stable-local-id",
      "type": "PROJECT|ARTIFACT|TOOL|PROCESS|GATE|MEMORY",
      "surface_form": "exact text from the document",
      "description": "short description grounded in the document",
      "source": {"document": "relative/path.md", "line": 1}
    }
  ],
  "relations": [
    {
      "subject": "stable-local-id",
      "predicate": "reads|writes|uses|requires|produces|gated_by|runs|contains",
      "object": "stable-local-id",
      "source": {"document": "relative/path.md", "line": 1}
    }
  ]
}
```

Rules:

1. Preserve the exact surface form; do not canonicalize aliases.
2. Use only entities and relations supported by text in the document.
3. Every entity and relation needs a source document and one-based line number.
4. Do not include Markdown headings, generic English words, or unsupported
   guesses as entities.
5. Return JSON only. No Markdown fence and no explanation outside the object.

Acceptance test for this corpus:
- If present, explicitly extract the surface forms `progress.md`, `spine`, and
  `committed spine` as separate mentions. They are intentionally not canonicalized.
- If present, explicitly extract `OpenCode` and `OpenCode CLI` as separate
  mentions. These are the duplicate families Project 3 measures.
- The document field must be exactly the supplied document identifier, copied
  without alteration.
