# Graph schema

All writes must preserve these invariants:

- claims are an array with unique IDs, subject/predicate/object, source,
  produced_by, and created fields;
- `source.kind` is `tool_output` or `inference`; only tool output can ground a
  factual reviewer verdict;
- runs have an ID, kind, evidence path, claim IDs, result, and version;
- existing array entries are append-only; corrections append a new claim with
  `supersedes` rather than editing the old one; and
- evidence files are raw captured output and are never rewritten.
