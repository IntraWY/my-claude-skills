#Requires -Version 5.1
<#
  install-rule.ps1 — ติดตั้ง visual-mockup global rule เข้า ~/.claude
  - copy rules/visual-mockup.md -> ~/.claude/rules/visual-mockup.md
  - เพิ่ม import "@rules/visual-mockup.md" ใน ~/.claude/CLAUDE.md (idempotent)
  รัน: powershell -ExecutionPolicy Bypass -File install-rule.ps1
#>
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$src = Join-Path $PSScriptRoot 'rules/visual-mockup.md'
if (-not (Test-Path $src)) {
    Write-Host "[ERROR] ไม่พบ $src — รันสคริปต์จากในโฟลเดอร์ repo ที่ clone มา" -ForegroundColor Red
    exit 1
}

$claudeDir  = Join-Path $HOME '.claude'
$rulesDir   = Join-Path $claudeDir 'rules'
$dest       = Join-Path $rulesDir 'visual-mockup.md'
$claudeMd   = Join-Path $claudeDir 'CLAUDE.md'
$importLine = '@rules/visual-mockup.md'

New-Item -ItemType Directory -Force -Path $rulesDir | Out-Null
Copy-Item -Path $src -Destination $dest -Force
Write-Host "[OK] copied rule -> $dest" -ForegroundColor Green

$utf8 = New-Object System.Text.UTF8Encoding($false)
if (Test-Path $claudeMd) {
    $content = [System.IO.File]::ReadAllText($claudeMd)
    $present = ($content -split "`r?`n") | Where-Object { $_.Trim() -eq $importLine }
    if ($present) {
        Write-Host "[SKIP] CLAUDE.md มี import อยู่แล้ว" -ForegroundColor Yellow
    } else {
        $prefix = if ($content.Length -gt 0 -and -not $content.EndsWith("`n")) { "`r`n" } else { "" }
        [System.IO.File]::AppendAllText($claudeMd, $prefix + $importLine + "`r`n", $utf8)
        Write-Host "[OK] เพิ่ม import ใน CLAUDE.md" -ForegroundColor Green
    }
} else {
    [System.IO.File]::WriteAllText($claudeMd, $importLine + "`r`n", $utf8)
    Write-Host "[OK] สร้าง CLAUDE.md พร้อม import" -ForegroundColor Green
}

Write-Host ""
Write-Host "เสร็จแล้ว ✅  เปิด session ใหม่ของ Claude Code ให้ rule โหลด" -ForegroundColor Cyan
