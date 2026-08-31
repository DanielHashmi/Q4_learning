param(
  [string]$Agent = "claude",   # "claude" or "opencode"
  [string]$PromptFile = "night-prompt.txt",
  [string]$LogFile = "night-run.log"
)

# Run the nightly triage loop against the current worktree.
# Reusable across runs/branches - no hardcoded paths, no throwaway wrappers.

if (-not (Test-Path $PromptFile)) {
  Write-Error "Prompt file not found: $PromptFile"
  exit 1
}

$prompt = Get-Content $PromptFile -Raw

switch ($Agent) {
  "claude" {
    $prompt | & claude -p --permission-mode auto --verbose --max-budget-usd 2 --output-format text *> $LogFile
  }
  "opencode" {
    $prompt | & opencode run --auto --model opencode/claude-sonnet-5 *> $LogFile
  }
  default {
    Write-Error "Unknown agent: $Agent (use 'claude' or 'opencode')"
    exit 1
  }
}

Add-Content $LogFile "EXITCODE=$LASTEXITCODE"
Write-Host "Run complete. See $LogFile"
