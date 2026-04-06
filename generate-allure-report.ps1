param(
    [string]$ResultsDir = "reports/allure-results",
    [string]$ReportBaseDir = "reports/generated-reports"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ResultsDir)) {
    throw "Allure results directory not found: $ResultsDir"
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportDir = Join-Path $ReportBaseDir $timestamp

New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

allure generate $ResultsDir -o $reportDir

Write-Host "Report saved to: $reportDir"
