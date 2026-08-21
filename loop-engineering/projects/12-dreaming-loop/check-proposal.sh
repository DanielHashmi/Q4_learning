#!/usr/bin/env bash
set -Eeuo pipefail
proposal_dir=${1:-proposal}
test -f "$proposal_dir/dreaming-report.md"
grep -Fq 'rules_changed_directly: no' "$proposal_dir/dreaming-report.md"
grep -Fq 'repeated_correction:' "$proposal_dir/dreaming-report.md"
test -f "$proposal_dir/proposed-rules-change.md"
test -f "$proposal_dir/proposed-deletion.md"
grep -Fq 'Cited run dates:' "$proposal_dir/proposed-rules-change.md"
grep -Fq 'Frequency:' "$proposal_dir/proposed-rules-change.md"
grep -Fq 'This is a proposal only' "$proposal_dir/proposed-rules-change.md"
grep -Fq 'Reason:' "$proposal_dir/proposed-deletion.md"
echo 'Project 12 checker passed: proposal has repeated evidence, citations, deletion, and no direct rules edit.'
