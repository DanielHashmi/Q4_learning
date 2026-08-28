# Entity-resolution contract

You are resolving extracted surface forms into canonical entities. Return only
one JSON object:

This is a batch execution request, not a request for clarification. Do not ask
questions, discuss the task, or explain your process. Produce the JSON object
now, even when a form must remain a singleton cluster.

```json
{
  "clusters": [
    {
      "canonical_id": "stable_id",
      "type": "ARTIFACT|TOOL|PROJECT|PROCESS|GATE|MEMORY",
      "aliases": [0, 4],
      "rationale": "evidence-based explanation",
      "confidence": 0.0
    }
  ]
}
```

`aliases` contains the integer indexes from the supplied surface-form array.
Every index must occur exactly once. Merge aliases only when their type,
description, and source context support the same real entity. Keep same-name
entities separate when their descriptions or roles differ. Never discard a
surface form. Return JSON only, without Markdown fences.
