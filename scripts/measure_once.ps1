[CmdletBinding()]
param([string]$OutputPath = (Join-Path $PWD ('gpower-first-call-'+[DateTime]::Now.ToString('yyyyMMdd_HHmmss_fffffff')+'.json')))
# Manual use after a user-controlled reboot. This script does not reboot or warm up.
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$resolved=(Get-Command gpower-clone -CommandType Application -ErrorAction Stop).Source
$start=[Diagnostics.ProcessStartInfo]::new()
$start.FileName=$resolved
$start.Arguments='--test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1'
$start.UseShellExecute=$false
$start.RedirectStandardOutput=$true
$start.RedirectStandardError=$true
$process=[Diagnostics.Process]::new()
$process.StartInfo=$start
$timer=[Diagnostics.Stopwatch]::StartNew()
if (-not $process.Start()) { throw 'CLI could not start.' }
$stdoutTask=$process.StandardOutput.ReadToEndAsync()
$stderrTask=$process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$stdout=$stdoutTask.GetAwaiter().GetResult()
$stderr=$stderrTask.GetAwaiter().GetResult()
$timer.Stop()
$receipt=[ordered]@{recorded_at=[DateTimeOffset]::Now.ToString('o');executable=$resolved;
    argv=$start.Arguments;cwd=$PWD.Path;elapsed_seconds=$timer.Elapsed.TotalSeconds;
    stdout=$stdout;stderr=$stderr;exit_code=$process.ExitCode;
    numerical_calls_by_script=1;preparation_by_script=$false;
    reboot_state='Not inferred; user must state whether reboot occurred before this manual run';
    os_disk_cache_cold_claim=$false}
$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
$process.Dispose()
Write-Output ($receipt | ConvertTo-Json -Depth 6)
if ($receipt.exit_code -ne 0) { exit $receipt.exit_code }
$result=$stdout | ConvertFrom-Json
if ($result.n1 -ne 105 -or $result.n2 -ne 105 -or $result.n_total -ne 210) { throw 'Unexpected calculation; evidence retained.' }
