#!/usr/bin/env bash
set -Eeuo pipefail

dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
trap 'rm -f "$dir/transcript-dotenv.txt" "$dir/transcript-environment.txt" "$dir/.env"' EXIT

printf 'PROJECT10_DUMMY_TOKEN=local-dummy-token\n' > "$dir/.env"
git -C "$dir/../../.." check-ignore -q "$dir/.env"
bash "$dir/run-secrets-drill.sh" dotenv >/dev/null
PROJECT10_DUMMY_TOKEN='local-dummy-token' bash "$dir/run-secrets-drill.sh" environment >/dev/null

grep -Fq 'infrastructure_status=GREEN' "$dir/transcript-dotenv.txt"
grep -Fq 'task_status=FAIL' "$dir/transcript-dotenv.txt"
grep -Fq 'fresh cloud clone' "$dir/transcript-dotenv.txt"
grep -Fq 'infrastructure_status=GREEN' "$dir/transcript-environment.txt"
grep -Fq 'task_status=PASS' "$dir/transcript-environment.txt"
grep -Fq 'read PROJECT10_DUMMY_TOKEN from environment' "$dir/transcript-environment.txt"
! grep -Fq 'local-dummy-token' "$dir/transcript-environment.txt"

echo 'Project 10 verification passed: ignored .env fails and environment injection succeeds.'
