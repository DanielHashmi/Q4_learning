# Proves the Docker network fence against the current directory.
# Run from the worktree you want to fence-test.
#
# Control: default networking - should CONNECT.
# Fenced:  --network=none      - should FAIL to resolve/connect.

$check = "const req=require('http').get({host:'example.com',timeout:8000}, r => {console.log('CONNECTED', r.statusCode); process.exit(0)}); req.on('timeout', () => {console.log('TIMEOUT'); process.exit(0)}); req.on('error', e => {console.log('FENCE HELD:', e.message); process.exit(0)})"

Write-Host "=== CONTROL (default network, should CONNECT) ==="
docker run --rm -v "${PWD}:/work" -w /work node:20-slim node -e $check

Write-Host ""
Write-Host "=== FENCED (--network=none, should FAIL) ==="
docker run --rm --network=none -v "${PWD}:/work" -w /work node:20-slim node -e $check
