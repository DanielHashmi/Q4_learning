#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
for file in "$root"/output/project-*.json; do
  jq -e '
    type == "object" and (.document | type == "string") and
    (.entities | type == "array") and (.relations | type == "array") and
    all(.entities[]; (.id | type == "string") and (.surface_form | type == "string") and
        (.type == "PROJECT" or .type == "ARTIFACT" or .type == "TOOL" or
         .type == "PROCESS" or .type == "GATE" or .type == "MEMORY") and
        (.source.document | type == "string") and (.source.line | type == "number")) and
    all(.relations[]; (.subject | type == "string") and (.object | type == "string") and
        (.predicate == "reads" or .predicate == "writes" or .predicate == "uses" or
         .predicate == "requires" or .predicate == "produces" or .predicate == "gated_by" or
         .predicate == "runs" or .predicate == "contains") and
        (.source.document | type == "string") and (.source.line | type == "number"))
  ' "$file" >/dev/null
  echo "jq schema PASS: $(basename "$file")"
done
