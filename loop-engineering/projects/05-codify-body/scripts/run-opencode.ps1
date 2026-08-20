param(
  [Parameter(Mandatory = $true)][string]$Directory,
  [Parameter(Mandatory = $true)][string]$DataHome,
  [Parameter(Mandatory = $true)][string]$ConfigHome,
  [Parameter(Mandatory = $true)][string]$StateHome,
  [Parameter(Mandatory = $true)][string]$OpenCode,
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$OpenCodeArgs
)

$ErrorActionPreference = 'Stop'

New-Item -ItemType Directory -Force -Path $DataHome, $ConfigHome, $StateHome | Out-Null
$env:XDG_DATA_HOME = $DataHome
$env:XDG_CONFIG_HOME = $ConfigHome
$env:XDG_STATE_HOME = $StateHome

& $OpenCode @OpenCodeArgs --dir $Directory
exit $LASTEXITCODE
