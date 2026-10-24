[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $PSScriptRoot '.run'),
    [string]$PythonVersion = '3.14.8',
    [string]$UvPath,
    [string]$PythonExecutable,
    [switch]$Offline,
    [string]$WheelPath,
    [string]$Wheelhouse,
    [string]$CacheDirectory,
    [switch]$NoPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$processPathBefore = $env:PATH
$targetRoot = [IO.Path]::GetFullPath($Destination)
$toolsRoot = Join-Path $targetRoot '.tools'
$uvRoot = Join-Path $toolsRoot 'uv'
$uvExe = Join-Path $uvRoot 'uv.exe'
$uvVersion = '0.13.4'
$installerUrl = "https://astral.sh/uv/$uvVersion/install.ps1"
$installerPath = Join-Path $toolsRoot 'uv-install.ps1'
if ($UvPath) { $uvExe = [IO.Path]::GetFullPath($UvPath) }
if ($WheelPath) { $WheelPath = [IO.Path]::GetFullPath($WheelPath) }
if ($Wheelhouse) { $Wheelhouse = [IO.Path]::GetFullPath($Wheelhouse) }
if ($Offline -and (-not $UvPath -or -not $PythonExecutable -or -not $WheelPath)) {
    throw 'Offline mode requires -UvPath, -PythonExecutable and -WheelPath; provide a compatible complete wheelhouse or populated uv cache.'
}
if ($WheelPath -and -not (Test-Path -LiteralPath $WheelPath -PathType Leaf)) { throw 'WheelPath does not exist.' }
$environmentNames = @('UV_UNMANAGED_INSTALL','UV_NO_MODIFY_PATH','UV_PYTHON_INSTALL_DIR',
    'UV_PYTHON_BIN_DIR','UV_PYTHON_INSTALL_REGISTRY','UV_CACHE_DIR','UV_PYTHON_PREFERENCE','UV_OFFLINE')
$previousEnvironment = @{}
foreach ($variableName in $environmentNames) {
    $previousEnvironment[$variableName] = [Environment]::GetEnvironmentVariable($variableName,'Process')
}

function Invoke-Uv([string[]]$Arguments) {
    & $uvExe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "uv failed with exit code $LASTEXITCODE" }
}

function Get-Sha256([string]$Path) {
    $algorithm = [Security.Cryptography.SHA256]::Create()
    $stream = [IO.File]::OpenRead($Path)
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
    finally { $stream.Dispose(); $algorithm.Dispose() }
}

function Normalize-PathEntry([string]$Entry) {
    $expanded = [Environment]::ExpandEnvironmentVariables($Entry.Trim().Trim('"'))
    try { $expanded = [IO.Path]::GetFullPath($expanded) } catch { }
    return $expanded.TrimEnd([char[]]'\/').ToUpperInvariant()
}

function Register-UserPath([string]$Directory) {
    $key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey('Environment')
    try {
        $old = [string]$key.GetValue('Path','',[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
        $kind = if ($key.GetValueNames() -contains 'Path') { $key.GetValueKind('Path') } else { [Microsoft.Win32.RegistryValueKind]::ExpandString }
        $entries = @($old -split ';' | Where-Object { $_.Trim() })
        $normalized = Normalize-PathEntry $Directory
        $present = @($entries | Where-Object { (Normalize-PathEntry $_) -eq $normalized }).Count -gt 0
        if (-not $present) {
            $separator = if (-not $old -or $old.EndsWith(';')) { '' } else { ';' }
            $key.SetValue('Path',($old + $separator + $Directory),$kind)
            Write-Output "Added to HKCU user PATH: $Directory"
        } else { Write-Output "Already in HKCU user PATH: $Directory" }
        $processEntries = @($env:PATH -split ';' | Where-Object { $_.Trim() })
        if (@($processEntries | Where-Object { (Normalize-PathEntry $_) -eq $normalized }).Count -eq 0) {
            $env:PATH = $Directory + ';' + $env:PATH
        }
        if (-not ('GPowerEnvironmentNotifier' -as [type])) {
            Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class GPowerEnvironmentNotifier {
    [DllImport("user32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    public static extern IntPtr SendMessageTimeout(IntPtr hwnd, uint message,
        UIntPtr wParam, string lParam, uint flags, uint timeout, out UIntPtr result);
}
'@
        }
        $notificationResult = [UIntPtr]::Zero
        $notificationStatus = [GPowerEnvironmentNotifier]::SendMessageTimeout(
            [IntPtr]0xffff,0x001a,[UIntPtr]::Zero,'Environment',2,2000,[ref]$notificationResult)
        Write-Output 'Sent WM_SETTINGCHANGE/Environment notification (2-second bounded timeout); existing terminals may retain their environment.'
        return [pscustomobject]@{ directory=$Directory; added=(-not $present); previous_user_path=$old;
            resulting_user_path=[string]$key.GetValue('Path','',[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames);
            environment_notification_attempted=$true; notification_return=$notificationStatus.ToInt64(); notification_timeout_ms=2000 }
    } finally { $key.Dispose() }
}

try {
    New-Item -ItemType Directory -Force $targetRoot,$toolsRoot,$uvRoot | Out-Null
    $env:UV_UNMANAGED_INSTALL = $uvRoot
    $env:UV_NO_MODIFY_PATH = '1'
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $toolsRoot 'python'
    $env:UV_PYTHON_BIN_DIR = Join-Path $toolsRoot 'python-bin'
    $env:UV_PYTHON_INSTALL_REGISTRY = 'false'
    $env:UV_CACHE_DIR = if ($CacheDirectory) { [IO.Path]::GetFullPath($CacheDirectory) } else { Join-Path $targetRoot '.cache' }
    if ($Offline) { $env:UV_OFFLINE = '1' }
    if (-not $PythonExecutable) { $env:UV_PYTHON_PREFERENCE = 'only-managed' }
    if (-not (Test-Path -LiteralPath $uvExe)) {
        # Official versioned installer; no existing uv or Python is required.
        Invoke-WebRequest -UseBasicParsing -Uri $installerUrl -OutFile $installerPath
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installerPath
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $uvExe)) {
            throw 'Official uv installation did not complete.'
        }
    }
    $actualUvVersion = (& $uvExe --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read uv version.' }
    if (-not $PythonExecutable) {
        Invoke-Uv @('python','install',$PythonVersion)
        $PythonExecutable = $PythonVersion
    }
    $venvPath = Join-Path $targetRoot '.venv'
    $pythonExe = Join-Path $venvPath 'Scripts\python.exe'
    $reusedEnvironment = Test-Path -LiteralPath $pythonExe -PathType Leaf
    if (-not $reusedEnvironment) {
        if (Test-Path -LiteralPath $venvPath) { throw 'Existing destination has no usable venv Python; choose another destination.' }
        Invoke-Uv @('venv','--python',$PythonExecutable,$venvPath)
    }
    $installArguments = @('pip','install','--compile-bytecode','--link-mode','copy','--python',$pythonExe)
    if ($Wheelhouse) { $installArguments += @('--no-index','--find-links',$Wheelhouse) }
    Invoke-Uv ($installArguments + @('-r',(Join-Path $projectRoot 'requirements.lock.txt')))
    if ($WheelPath) {
        Invoke-Uv ($installArguments + @('--no-deps',$WheelPath))
    } else {
        Invoke-Uv ($installArguments + @('--no-deps','--no-build-isolation',$projectRoot))
    }
    # Filesystem-only cache probe, then exactly one real installed-CLI calculation.
    $cliExe = Join-Path $venvPath 'Scripts\gpower-clone.exe'
    $preparationReceiptPath = Join-Path $targetRoot 'PREPARATION_RECEIPT.json'
    $cacheProbePath = Join-Path $targetRoot 'PREPARATION_PYCACHE_BEFORE.json'
    & $pythonExe -I (Join-Path $projectRoot 'scripts/prepare_runtime.py') --cli $cliExe --receipt $preparationReceiptPath --probe $cacheProbePath
    if ($LASTEXITCODE -ne 0) { throw 'Installed CLI preparation failed; installation is not successful. See PREPARATION_RECEIPT.json.' }
    $preparation = [IO.File]::ReadAllText($preparationReceiptPath) | ConvertFrom-Json
    if (-not $preparation.success) { throw 'Installed CLI preparation validation failed.' }
    Invoke-Uv @('pip','check','--python',$pythonExe)
    $actualPythonVersion = (& $pythonExe --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read installed Python version.' }
    $cliExe = Join-Path $venvPath 'Scripts\gpower-clone.exe'
    # Version check is additional to the explicitly recorded first numerical preparation.
    $versionTimer = [Diagnostics.Stopwatch]::StartNew()
    $versionOutput = (& $cliExe --version | Out-String).Trim()
    $versionExitCode = $LASTEXITCODE
    $versionTimer.Stop()
    if ($versionExitCode -ne 0) { throw 'Installed CLI version query failed.' }
    $result = $versionOutput | ConvertFrom-Json
    if ($result.contract_version -ne '1.0.0' -or $result.name -ne 'Takim 20 - Ismail Burak Yilmaz') { throw 'Unexpected CLI identity.' }
    $pathRegistration = $null
    if (-not $NoPath) {
        # User explicitly authorized HKCU and this process; HKLM is never written.
        $pathMessages = @(Register-UserPath (Join-Path $venvPath 'Scripts'))
        foreach ($message in $pathMessages) { if ($message -is [string]) { Write-Output $message } else { $pathRegistration = $message } }
    }
    $receipt = [ordered]@{
        source = $projectRoot; destination = $targetRoot
        official_uv_installer = $installerUrl
        uv_installer_sha256 = if (Test-Path -LiteralPath $installerPath) { Get-Sha256 $installerPath } else { $null }
        uv = $actualUvVersion; python = $actualPythonVersion
        python_requested = $PythonVersion; managed_python_directory = $env:UV_PYTHON_INSTALL_DIR
        python_executable = $pythonExe; cli_executable = $cliExe
        requirements_sha256 = Get-Sha256 (Join-Path $projectRoot 'requirements.lock.txt')
        version = $result; version_elapsed_seconds = $versionTimer.Elapsed.TotalSeconds
        version_exit_code = $versionExitCode; numerical_warmup_performed = $true
        preparation = $preparation; preparation_receipt = $preparationReceiptPath
        preparation_is_first_numerical_call_in_this_installation = $true
        preparation_is_first_ever_in_venv = (-not $reusedEnvironment)
        preparation_context = if ($reusedEnvironment) { 'Reused venv: previous numerical calls existed; not a first-ever/cold claim' } else { 'New empty venv: this is its first numerical call; OS cache state is unknown' }
        preparation_cost_is_installation = $true
        compile_bytecode = $true; offline = [bool]$Offline; wheel = $WheelPath
        reused_environment = [bool]$reusedEnvironment
        dependency_check_exit_code = 0; no_path = [bool]$NoPath; path_registration=$pathRegistration
        process_path_before=$processPathBefore; process_path_after=$env:PATH
        scope = 'project-local environment; only HKCU user PATH and this process PATH registered unless NoPath; HKLM/profile unchanged'
    }
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $targetRoot 'INSTALLATION_RECEIPT.json') -Encoding UTF8
    Write-Output $versionOutput
    Write-Output "Installed: $pythonExe"
    if ($NoPath) { Write-Output 'NoPath: PATH registration skipped. Project-root fallback: .\gpower-clone.cmd --version' }
    else { Write-Output 'Only HKCU user PATH and this process PATH updated. Existing parent shells keep their environment; refresh PATH from User+Machine or start a fresh environment.' }
}
finally {
    foreach ($variableName in $environmentNames) {
        [Environment]::SetEnvironmentVariable($variableName,$previousEnvironment[$variableName],'Process')
    }
}
