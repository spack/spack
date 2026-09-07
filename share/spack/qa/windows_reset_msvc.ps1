# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

<#
.SYNOPSIS
    Reset a Windows host to a pristine "no MSVC" state for Spack.

.DESCRIPTION
    Removes Visual Studio / Build Tools installations and the stale artifacts they leave
    behind, so that Spack's Windows compiler detection and clingo bootstrap can be
    validated from a known-clean starting point.

    The script never guesses: every action is reported, and a verification pass re-checks
    the host after the actions have run. It exits non-zero if the host is not clean or if
    any step failed.

    Cleanup targets, in order:
      1. Visual Studio / Build Tools instances reported by vswhere (uninstalled via vs_installer,
         -Force only).
      2. Instances that survive step 1 (Microsoft's InstallCleanup.exe, -RunInstallCleanup only).
      3. Leftover "Microsoft Visual Studio" directories under Program Files.
      4. Visual Studio Installer instance metadata (_Instances).
      5. Stale instance-suffixed VisualStudio registry keys whose install paths no longer exist.
         These are read by spack.operating_systems.windows_os and cause phantom detections.
      6. Stale msvc / win-sdk / wgl / win-wdk externals in Spack's user packages.yaml.
      7. Spack's bootstrap store.

    Not touched: Visual C++ redistributables (needed by unrelated software), the Visual Studio
    Installer itself (needed to reinstall Build Tools), and Windows Kits. Use
    -IncludeWindowsKits for a read-only report of the Windows Kits state.

    Processes running from inside a directory that is about to be removed (for example
    VCTIP.EXE, which cl.exe spawns) are stopped so they cannot hold files open.

.PARAMETER Apply
    Perform the cleanup. Without this switch the script only reports what it would do.

.PARAMETER Force
    Allow last-resort direct removal of leftover directories and registry keys when the
    vendor uninstallers cannot or will not remove them, and allow uninstalling Visual Studio
    instances that are still registered. Requires -Apply. Requires elevation for machine-wide
    paths and HKLM keys.

.PARAMETER RunInstallCleanup
    Allow Microsoft's InstallCleanup.exe to run when an instance survives a failed uninstall.
    Opt-in, because InstallCleanup removes an instance wholesale -- including a healthy one
    that the uninstall step merely failed to talk to. Requires -Apply and -Force.

.PARAMETER Elevate
    Relaunch the script with an administrator token (UAC prompt) and stream the elevated
    run's output back to this console. Assumes UAC elevates the same user account; if a
    different administrator account is used, the Spack user config steps will act on that
    account's profile.

.PARAMETER KeepSpackConfig
    Do not modify Spack's user packages.yaml.

.PARAMETER CleanSpackCaches
    Run "spack clean -a" instead of only clearing the bootstrap store.

.PARAMETER IncludeWindowsKits
    Additionally report the Windows Kits (SDK/WDK) state. Read-only: Windows Kits are never
    removed by this script.

.PARAMETER SpackRoot
    Path to the Spack checkout. Defaults to the checkout containing this script.

.EXAMPLE
    .\share\spack\qa\windows_reset_msvc.ps1
    Report what would be cleaned, change nothing.

.EXAMPLE
    .\share\spack\qa\windows_reset_msvc.ps1 -Apply -Force -Elevate
    Prompt for elevation and fully reset the host.
#>

#Requires -Version 5.1

[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$Force,
    [switch]$RunInstallCleanup,
    [switch]$Elevate,
    [switch]$KeepSpackConfig,
    [switch]$CleanSpackCaches,
    [switch]$IncludeWindowsKits,
    [string]$SpackRoot
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'

# Package names whose externals become invalid once the toolchain is removed.
$SpackStalePackages = @('msvc', 'win-sdk', 'wgl', 'win-wdk')

# Instance-suffixed registry key names, e.g. "17.0_cc287979". Unsuffixed keys such as
# "14.0" are shared/legacy and are never removed.
$InstanceKeyPattern = '^\d+\.\d+_[0-9a-fA-F]+$'

$script:Actions = New-Object System.Collections.ArrayList
$script:Checks = New-Object System.Collections.ArrayList

function Add-Action {
    param([string]$Step, [string]$Item, [string]$Status, [string]$Detail = '')
    $null = $script:Actions.Add([pscustomobject]@{
            Step   = $Step
            Item   = $Item
            Status = $Status
            Detail = $Detail
        })
}

function Add-Check {
    param([string]$Check, [bool]$Passed, [string]$Detail = '')
    $null = $script:Checks.Add([pscustomobject]@{
            Check  = $Check
            Result = $(if ($Passed) { 'CLEAN' } else { 'DIRTY' })
            Detail = $Detail
        })
}

function Test-Elevated {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-ProgramFilesRoots {
    $roots = @()
    foreach ($var in 'ProgramFiles', 'ProgramFiles(x86)') {
        $value = [Environment]::GetEnvironmentVariable($var)
        if ($value -and ($roots -notcontains $value)) { $roots += $value }
    }
    return $roots
}

function Get-VsInstallerDirectory {
    foreach ($root in Get-ProgramFilesRoots) {
        $dir = Join-Path $root 'Microsoft Visual Studio\Installer'
        if (Test-Path -LiteralPath $dir) { return $dir }
    }
    return $null
}

function Get-VsInstances {
    $installerDir = Get-VsInstallerDirectory
    if (-not $installerDir) { return @() }
    $vswhere = Join-Path $installerDir 'vswhere.exe'
    if (-not (Test-Path -LiteralPath $vswhere)) { return @() }

    $raw = & $vswhere -all -prerelease -products '*' -format json 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "vswhere.exe exited with $LASTEXITCODE"
        return @()
    }
    $text = ($raw | Out-String).Trim()
    if (-not $text) { return @() }
    try {
        $parsed = $text | ConvertFrom-Json
    } catch {
        Write-Warning "could not parse vswhere output: $($_.Exception.Message)"
        return @()
    }
    if ($null -eq $parsed) { return @() }
    return @($parsed)
}

function Get-VsRootDirectories {
    $dirs = @()
    foreach ($root in Get-ProgramFilesRoots) {
        $vsRoot = Join-Path $root 'Microsoft Visual Studio'
        if (-not (Test-Path -LiteralPath $vsRoot)) { continue }
        foreach ($child in Get-ChildItem -LiteralPath $vsRoot -Directory -ErrorAction SilentlyContinue) {
            # The Installer directory hosts vswhere/vs_installer and must survive.
            if ($child.Name -eq 'Installer') { continue }
            $dirs += $child.FullName
        }
    }
    return $dirs
}

function Get-ClExecutables {
    $found = @()
    foreach ($root in Get-ProgramFilesRoots) {
        $vsRoot = Join-Path $root 'Microsoft Visual Studio'
        if (-not (Test-Path -LiteralPath $vsRoot)) { continue }
        $found += Get-ChildItem -LiteralPath $vsRoot -Filter 'cl.exe' -Recurse -File -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty FullName
    }
    return $found
}

function Get-StaleVsRegistryKeys {
    <#
        Returns registry keys that describe a Visual Studio instance which is no longer on
        disk. Two shapes are handled:
          HKLM\SOFTWARE\[WOW6432Node\]Microsoft\VisualStudio_<hash>  (Capabilities/ApplicationDescription)
          HKLM\SOFTWARE\[WOW6432Node\]Microsoft\VisualStudio\<ver>_<hash>  (InstallDir/ShellFolder/ProductDir)
    #>
    $stale = @()
    $parents = @(
        'HKLM:\SOFTWARE\Microsoft',
        'HKLM:\SOFTWARE\WOW6432Node\Microsoft'
    )

    foreach ($parent in $parents) {
        if (-not (Test-Path -LiteralPath $parent)) { continue }

        foreach ($key in Get-ChildItem -LiteralPath $parent -ErrorAction SilentlyContinue) {
            if ($key.PSChildName -notmatch '^VisualStudio_[0-9a-fA-F]+$') { continue }
            $capabilities = Join-Path $key.PSPath 'Capabilities'
            $target = $null
            if (Test-Path -LiteralPath $capabilities) {
                $props = Get-ItemProperty -LiteralPath $capabilities -ErrorAction SilentlyContinue
                if ($props -and $props.PSObject.Properties.Name -contains 'ApplicationDescription') {
                    # Value looks like "@C:\...\devenv.exe,-12345"
                    $target = ($props.ApplicationDescription -split ',')[0].TrimStart('@')
                }
            }
            if (-not $target -or -not (Test-Path -LiteralPath $target)) {
                $detail = if ($target) { "target missing: $target" } else { 'no ApplicationDescription target' }
                $stale += [pscustomobject]@{ Path = $key.PSPath; Name = $key.Name; Detail = $detail }
            }
        }

        $vsKey = Join-Path $parent 'VisualStudio'
        if (-not (Test-Path -LiteralPath $vsKey)) { continue }
        foreach ($key in Get-ChildItem -LiteralPath $vsKey -ErrorAction SilentlyContinue) {
            if ($key.PSChildName -notmatch $InstanceKeyPattern) { continue }
            $props = Get-ItemProperty -LiteralPath $key.PSPath -ErrorAction SilentlyContinue
            $target = $null
            foreach ($name in 'InstallDir', 'ShellFolder', 'ProductDir') {
                if ($props -and ($props.PSObject.Properties.Name -contains $name) -and $props.$name) {
                    $target = $props.$name
                    break
                }
            }
            if (-not $target -or -not (Test-Path -LiteralPath $target)) {
                $detail = if ($target) { "target missing: $target" } else { 'no install path value' }
                $stale += [pscustomobject]@{ Path = $key.PSPath; Name = $key.Name; Detail = $detail }
            }
        }
    }
    return $stale
}

function Invoke-Tool {
    param([string]$FilePath, [string[]]$ArgumentList, [switch]$Stream)

    # -Stream echoes each line as it arrives; uninstallers can run for many minutes and are
    # indistinguishable from a hang when their output is only reported at the end.
    $lines = New-Object System.Collections.ArrayList
    & $FilePath @ArgumentList 2>&1 | ForEach-Object {
        $line = "$_"
        if ($Stream -and $line.Trim()) { Write-Host "     $line" }
        $null = $lines.Add($line)
    }
    return @{ ExitCode = $LASTEXITCODE; Output = ($lines -join [Environment]::NewLine).Trim() }
}

function Get-SpackCommand {
    if ($SpackRoot) {
        $candidate = Join-Path $SpackRoot 'bin\spack.ps1'
        if (Test-Path -LiteralPath $candidate) { return $candidate }
        Write-Warning "no bin\spack.ps1 under -SpackRoot '$SpackRoot'"
        return $null
    }
    $candidate = Join-Path $PSScriptRoot '..\..\..\bin\spack.ps1'
    if (Test-Path -LiteralPath $candidate) { return (Resolve-Path -LiteralPath $candidate).Path }
    if ($env:SPACK_ROOT) {
        $candidate = Join-Path $env:SPACK_ROOT 'bin\spack.ps1'
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    return $null
}

function Invoke-Spack {
    param([string]$SpackCmd, [string[]]$ArgumentList)
    $output = & $SpackCmd @ArgumentList 2>&1
    return @{ ExitCode = $LASTEXITCODE; Output = ($output | Out-String).Trim() }
}

function Get-SpackUserConfigPath {
    param([string]$SpackCmd)
    if ($SpackCmd) {
        $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList @(
            'python', '-c', 'import spack.paths; print(spack.paths.user_config_path)')
        if ($result.ExitCode -eq 0 -and $result.Output) {
            $line = ($result.Output -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 1).Trim()
            if ($line) { return $line }
        }
    }
    if ($env:SPACK_USER_CONFIG_PATH) { return $env:SPACK_USER_CONFIG_PATH }
    return (Join-Path $env:USERPROFILE '.spack')
}

function Stop-ProcessesUnderPath {
    param([string]$Path)

    # Toolchain helpers such as VCTIP.EXE (spawned by cl.exe) keep DLLs in the toolset directory
    # mapped, which makes deletion fail with "Access is denied" even for administrators.
    $prefix = $Path.TrimEnd('\') + '\'
    $running = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
            $_.Path -and $_.Path.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
        })
    foreach ($proc in $running) {
        $label = "$($proc.ProcessName)($($proc.Id))"
        try {
            Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            Add-Action -Step 'stop-process' -Item $label -Status 'Ok' -Detail $proc.Path
        } catch {
            Add-Action -Step 'stop-process' -Item $label -Status 'Failed' -Detail $_.Exception.Message
        }
    }
    if ($running.Count -gt 0) { Start-Sleep -Seconds 2 }
    return $running.Count
}

function Remove-ItemReported {
    param([string]$Step, [string]$Path, [string]$Reason, [bool]$RequireForce = $true)

    if (-not (Test-Path -LiteralPath $Path)) {
        Add-Action -Step $Step -Item $Path -Status 'NotNeeded' -Detail 'already absent'
        return
    }
    if (-not $Apply) {
        Add-Action -Step $Step -Item $Path -Status 'DryRun' -Detail $Reason
        return
    }
    if ($RequireForce -and -not $Force) {
        Add-Action -Step $Step -Item $Path -Status 'Skipped' -Detail 'needs -Force'
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step $Step -Item $Path -Status 'Skipped' -Detail 'needs elevation'
        return
    }
    try {
        Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction Stop
        Add-Action -Step $Step -Item $Path -Status 'Ok' -Detail $Reason
        return
    } catch {
        $failure = $_.Exception.Message
    }
    if ((Stop-ProcessesUnderPath -Path $Path) -gt 0) {
        try {
            Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction Stop
            Add-Action -Step $Step -Item $Path -Status 'Ok' -Detail "$Reason (after releasing file locks)"
            return
        } catch {
            $failure = $_.Exception.Message
        }
    }
    Add-Action -Step $Step -Item $Path -Status 'Failed' -Detail $failure
}

# ---------------------------------------------------------------------------------------
# Step 1: uninstall Visual Studio / Build Tools instances via the vendor installer
# ---------------------------------------------------------------------------------------

#: Set when an uninstall was attempted and the instance survived. InstallCleanup is only ever
#: allowed after that, so a healthy instance can never be removed by the fallback.
$script:UninstallLeftInstance = $false

function Wait-ForVsInstanceRemoval {
    param([string]$InstallPath, [int]$TimeoutSeconds = 1800)

    $start = Get-Date
    $deadline = $start.AddSeconds($TimeoutSeconds)
    $nextHeartbeat = $start.AddSeconds(30)
    while ((Get-Date) -lt $deadline) {
        $remaining = @(Get-VsInstances | Where-Object { $_.installationPath -eq $InstallPath })
        if ($remaining.Count -eq 0) { return $true }
        Start-Sleep -Seconds 5
        if ((Get-Date) -ge $nextHeartbeat) {
            Write-Step ('still uninstalling ({0:n0}s elapsed)' -f ((Get-Date) - $start).TotalSeconds)
            $nextHeartbeat = (Get-Date).AddSeconds(30)
        }
    }
    return $false
}

function Invoke-UninstallVsInstances {
    # @() is required: PowerShell unrolls a single-element return value, and .Count on a bare
    # PSCustomObject is $null in Windows PowerShell 5.1.
    $instances = @(Get-VsInstances)
    if ($instances.Count -eq 0) {
        Add-Action -Step 'vs-instances' -Item '(none)' -Status 'NotNeeded' -Detail 'vswhere reports no instances'
        return
    }

    $installerDir = Get-VsInstallerDirectory
    $vsInstaller = if ($installerDir) { Join-Path $installerDir 'vs_installer.exe' } else { $null }

    foreach ($instance in $instances) {
        $path = $instance.installationPath
        $label = "$($instance.displayName) [$path]"

        if (-not $Apply) {
            Add-Action -Step 'vs-instances' -Item $label -Status 'DryRun' -Detail 'would uninstall'
            continue
        }
        if (-not $Force) {
            Add-Action -Step 'vs-instances' -Item $label -Status 'Skipped' `
                -Detail 'needs -Force; refusing to uninstall a registered instance implicitly'
            continue
        }
        if (-not $vsInstaller -or -not (Test-Path -LiteralPath $vsInstaller)) {
            Add-Action -Step 'vs-instances' -Item $label -Status 'Failed' -Detail 'vs_installer.exe not found'
            continue
        }
        if (-not (Test-Elevated)) {
            Add-Action -Step 'vs-instances' -Item $label -Status 'Skipped' -Detail 'needs elevation'
            continue
        }

        # No --wait: setup.exe rejects it for 'uninstall' (exit 87) and the installer detaches,
        # so completion is observed through vswhere instead.
        Write-Step "uninstalling $path (this takes a while)"
        $result = Invoke-Tool -Stream -FilePath $vsInstaller -ArgumentList @(
            'uninstall', '--installPath', $path, '--quiet', '--norestart')

        if ($result.ExitCode -eq 87) {
            $script:UninstallLeftInstance = $true
            Add-Action -Step 'vs-instances' -Item $label -Status 'Failed' `
                -Detail "installer rejected the command line (87): $($result.Output)"
            continue
        }
        if ($result.ExitCode -eq 1602) {
            $script:UninstallLeftInstance = $true
            Add-Action -Step 'vs-instances' -Item $label -Status 'Failed' -Detail 'cancelled by user (1602)'
            continue
        }
        if ($result.ExitCode -ne 0 -and $result.ExitCode -ne 3010) {
            $script:UninstallLeftInstance = $true
            Add-Action -Step 'vs-instances' -Item $label -Status 'Failed' `
                -Detail "exit $($result.ExitCode): $($result.Output)"
            continue
        }

        if (Wait-ForVsInstanceRemoval -InstallPath $path) {
            Add-Action -Step 'vs-instances' -Item $label -Status 'Ok' -Detail 'uninstalled'
        } else {
            $script:UninstallLeftInstance = $true
            Add-Action -Step 'vs-instances' -Item $label -Status 'Failed' `
                -Detail 'still registered after the uninstall timeout'
        }
    }
}

# ---------------------------------------------------------------------------------------
# Step 2: Microsoft's own last-resort cleanup for instances the uninstaller cannot remove
# ---------------------------------------------------------------------------------------

function Invoke-InstallCleanup {
    $remaining = @(Get-VsInstances)
    if ($remaining.Count -eq 0) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'NotNeeded' -Detail 'no instances remain'
        return
    }
    if (-not $script:UninstallLeftInstance) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Skipped' `
            -Detail 'no uninstall attempt failed; the remaining instance is not known to be broken'
        return
    }

    $installerDir = Get-VsInstallerDirectory
    $cleanup = if ($installerDir) { Join-Path $installerDir 'InstallCleanup.exe' } else { $null }
    if (-not $cleanup -or -not (Test-Path -LiteralPath $cleanup)) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Skipped' -Detail 'not present'
        return
    }
    if (-not $Apply) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'DryRun' `
            -Detail "would run for $($remaining.Count) leftover instance(s)"
        return
    }
    if (-not $Force -or -not $RunInstallCleanup) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Skipped' `
            -Detail 'needs -Force and -RunInstallCleanup'
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Skipped' -Detail 'needs elevation'
        return
    }

    Write-Step 'running InstallCleanup.exe'
    $result = Invoke-Tool -Stream -FilePath $cleanup -ArgumentList @('-i')
    if ($result.ExitCode -eq 0) {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Ok' -Detail 'instance data removed'
    } else {
        Add-Action -Step 'install-cleanup' -Item 'InstallCleanup.exe' -Status 'Failed' `
            -Detail "exit $($result.ExitCode): $($result.Output)"
    }
}

# ---------------------------------------------------------------------------------------
# Step 3/4: leftover directories and installer metadata
# ---------------------------------------------------------------------------------------

function Invoke-RemoveLeftoverDirectories {
    $dirs = @(Get-VsRootDirectories)
    if ($dirs.Count -eq 0) {
        Add-Action -Step 'leftover-dirs' -Item '(none)' -Status 'NotNeeded' -Detail 'no leftover VS directories'
        return
    }
    foreach ($dir in $dirs) {
        $entries = @(Get-ChildItem -LiteralPath $dir -Force -Recurse -ErrorAction SilentlyContinue)
        $isEmpty = $entries.Count -eq 0
        $reason = if ($isEmpty) { 'empty leftover directory' } else { "$($entries.Count) leftover entries" }
        Remove-ItemReported -Step 'leftover-dirs' -Path $dir -Reason $reason -RequireForce (-not $isEmpty)
    }
}

function Invoke-RemoveInstallerMetadata {
    $instancesDir = Join-Path $env:ProgramData 'Microsoft\VisualStudio\Packages\_Instances'
    Remove-ItemReported -Step 'installer-metadata' -Path $instancesDir -Reason 'stale instance metadata'
}

# ---------------------------------------------------------------------------------------
# Step 5: stale registry keys that make Spack detect a phantom compiler
# ---------------------------------------------------------------------------------------

function Invoke-RemoveStaleRegistryKeys {
    $stale = @(Get-StaleVsRegistryKeys)
    if ($stale.Count -eq 0) {
        Add-Action -Step 'registry' -Item '(none)' -Status 'NotNeeded' -Detail 'no stale VisualStudio keys'
        return
    }
    foreach ($key in $stale) {
        if (-not $Apply) {
            Add-Action -Step 'registry' -Item $key.Name -Status 'DryRun' -Detail $key.Detail
            continue
        }
        if (-not $Force) {
            Add-Action -Step 'registry' -Item $key.Name -Status 'Skipped' -Detail 'needs -Force'
            continue
        }
        if (-not (Test-Elevated)) {
            Add-Action -Step 'registry' -Item $key.Name -Status 'Skipped' -Detail 'needs elevation'
            continue
        }
        try {
            Remove-Item -LiteralPath $key.Path -Recurse -Force -ErrorAction Stop
            Add-Action -Step 'registry' -Item $key.Name -Status 'Ok' -Detail $key.Detail
        } catch {
            Add-Action -Step 'registry' -Item $key.Name -Status 'Failed' -Detail $_.Exception.Message
        }
    }
}

# ---------------------------------------------------------------------------------------
# Step 6/7: Spack state
# ---------------------------------------------------------------------------------------

function Invoke-CleanSpackConfig {
    param([string]$SpackCmd, [string]$UserConfigPath)

    $packagesYaml = Join-Path $UserConfigPath 'packages.yaml'
    if (-not (Test-Path -LiteralPath $packagesYaml)) {
        Add-Action -Step 'spack-config' -Item $packagesYaml -Status 'NotNeeded' -Detail 'no user packages.yaml'
        return
    }

    $content = Get-Content -LiteralPath $packagesYaml -Raw -ErrorAction SilentlyContinue
    $present = @($SpackStalePackages | Where-Object { $content -match ('(?m)^\s{2}' + [regex]::Escape($_) + ':\s*$') })
    if ($present.Count -eq 0) {
        Add-Action -Step 'spack-config' -Item $packagesYaml -Status 'NotNeeded' -Detail 'no toolchain externals present'
        return
    }
    if (-not $Apply) {
        Add-Action -Step 'spack-config' -Item $packagesYaml -Status 'DryRun' `
            -Detail "would remove: $($present -join ', ')"
        return
    }

    $backup = "$packagesYaml.bak-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
    try {
        Copy-Item -LiteralPath $packagesYaml -Destination $backup -ErrorAction Stop
        Add-Action -Step 'spack-config' -Item $backup -Status 'Ok' -Detail 'backup written'
    } catch {
        Add-Action -Step 'spack-config' -Item $backup -Status 'Failed' -Detail $_.Exception.Message
        return
    }

    if (-not $SpackCmd) {
        Add-Action -Step 'spack-config' -Item 'spack config rm' -Status 'Skipped' `
            -Detail 'spack not found; pass -SpackRoot'
        return
    }
    foreach ($name in $present) {
        $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList @('config', 'rm', "packages:$name")
        if ($result.ExitCode -eq 0) {
            Add-Action -Step 'spack-config' -Item "packages:$name" -Status 'Ok' -Detail 'removed'
        } else {
            Add-Action -Step 'spack-config' -Item "packages:$name" -Status 'Failed' `
                -Detail "exit $($result.ExitCode): $($result.Output)"
        }
    }
}

function Invoke-CleanSpackStore {
    param([string]$SpackCmd)

    $spackArgs = if ($CleanSpackCaches) { @('clean', '-a') } else { @('clean', '-b') }
    $label = 'spack ' + ($spackArgs -join ' ')

    if (-not $SpackCmd) {
        Add-Action -Step 'spack-store' -Item $label -Status 'Skipped' -Detail 'spack not found; pass -SpackRoot'
        return
    }
    if (-not $Apply) {
        Add-Action -Step 'spack-store' -Item $label -Status 'DryRun' -Detail 'would clear bootstrap store'
        return
    }
    $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList $spackArgs
    if ($result.ExitCode -eq 0) {
        Add-Action -Step 'spack-store' -Item $label -Status 'Ok' -Detail 'cleared'
    } else {
        Add-Action -Step 'spack-store' -Item $label -Status 'Failed' `
            -Detail "exit $($result.ExitCode): $($result.Output)"
    }
}

# ---------------------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------------------

function Invoke-Verification {
    param([string]$SpackCmd, [string]$UserConfigPath)

    $instances = @(Get-VsInstances)
    Add-Check -Check 'no Visual Studio instances (vswhere)' -Passed ($instances.Count -eq 0) `
        -Detail $(if ($instances.Count -eq 0) { 'none' } else { ($instances | ForEach-Object { $_.installationPath }) -join '; ' })

    $cls = @(Get-ClExecutables)
    Add-Check -Check 'no cl.exe under Program Files\Microsoft Visual Studio' -Passed ($cls.Count -eq 0) `
        -Detail $(if ($cls.Count -eq 0) { 'none' } else { $cls -join '; ' })

    $dirs = @(Get-VsRootDirectories)
    Add-Check -Check 'no leftover Visual Studio directories' -Passed ($dirs.Count -eq 0) `
        -Detail $(if ($dirs.Count -eq 0) { 'none' } else { $dirs -join '; ' })

    $stale = @(Get-StaleVsRegistryKeys)
    Add-Check -Check 'no stale VisualStudio registry keys' -Passed ($stale.Count -eq 0) `
        -Detail $(if ($stale.Count -eq 0) { 'none' } else { ($stale | ForEach-Object { $_.Name }) -join '; ' })

    $instancesDir = Join-Path $env:ProgramData 'Microsoft\VisualStudio\Packages\_Instances'
    $instanceEntries = @()
    if (Test-Path -LiteralPath $instancesDir) {
        $instanceEntries = @(Get-ChildItem -LiteralPath $instancesDir -Force -ErrorAction SilentlyContinue)
    }
    Add-Check -Check 'no Visual Studio installer instance metadata' -Passed ($instanceEntries.Count -eq 0) `
        -Detail $(if ($instanceEntries.Count -eq 0) { 'absent or empty' } else { "$($instanceEntries.Count) entries in $instancesDir" })

    if (-not $KeepSpackConfig) {
        $packagesYaml = Join-Path $UserConfigPath 'packages.yaml'
        $present = @()
        if (Test-Path -LiteralPath $packagesYaml) {
            $content = Get-Content -LiteralPath $packagesYaml -Raw -ErrorAction SilentlyContinue
            $present = @($SpackStalePackages | Where-Object { $content -match ('(?m)^\s{2}' + [regex]::Escape($_) + ':\s*$') })
        }
        Add-Check -Check 'no toolchain externals in user packages.yaml' -Passed ($present.Count -eq 0) `
            -Detail $(if ($present.Count -eq 0) { 'none' } else { $present -join ', ' })
    }

    if ($SpackCmd) {
        $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList @(
            'python', '-c',
            'import spack.operating_systems.windows_os as w; print(w.WindowsOs().compiler_search_paths)')
        if ($result.ExitCode -ne 0) {
            Add-Check -Check 'Spack finds no MSVC search paths' -Passed $false `
                -Detail "spack python failed: $($result.Output)"
        } else {
            $line = ($result.Output -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 1).Trim()
            Add-Check -Check 'Spack finds no MSVC search paths' -Passed ($line -eq '[]') -Detail $line
        }
    } else {
        Add-Check -Check 'Spack finds no MSVC search paths' -Passed $false -Detail 'spack not found; pass -SpackRoot'
    }
}

function Write-WindowsKitsReport {
    $kitsRoot = Join-Path ${env:ProgramFiles(x86)} 'Windows Kits\10'
    Write-Host ''
    Write-Host '=== Windows Kits (read-only report; never removed by this script) ===' -ForegroundColor Cyan
    if (-not (Test-Path -LiteralPath $kitsRoot)) {
        Write-Host "  not present: $kitsRoot"
        return
    }
    Write-Host "  root: $kitsRoot"
    $libRoot = Join-Path $kitsRoot 'Lib'
    if (Test-Path -LiteralPath $libRoot) {
        foreach ($version in Get-ChildItem -LiteralPath $libRoot -Directory -ErrorAction SilentlyContinue) {
            $subs = @(Get-ChildItem -LiteralPath $version.FullName -Directory -ErrorAction SilentlyContinue |
                    Select-Object -ExpandProperty Name)
            $hasUcrtX64 = Test-Path -LiteralPath (Join-Path $version.FullName 'ucrt\x64')
            $hasWglX64 = Test-Path -LiteralPath (Join-Path $version.FullName 'um\x64\OpenGL32.Lib')
            Write-Host ("  {0}: [{1}] ucrt\x64={2} um\x64\OpenGL32.Lib={3}" -f `
                    $version.Name, ($subs -join ','), $hasUcrtX64, $hasWglX64)
        }
    }
    Write-Host '  To remove Windows Kits, use Settings > Apps > Installed apps (Windows SDK / WDK).'
}

# ---------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------

function Write-Step {
    param([string]$Message)
    Write-Host "  -> $Message" -ForegroundColor DarkGray
}

function Write-NewLogLines {
    param([string]$Path, [int]$AlreadyShown)

    if (-not (Test-Path -LiteralPath $Path)) { return $AlreadyShown }
    $lines = @(Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue)
    if ($lines.Count -le $AlreadyShown) { return $AlreadyShown }
    $lines[$AlreadyShown..($lines.Count - 1)] | ForEach-Object { Write-Host $_ }
    return $lines.Count
}

function Invoke-SelfElevate {
    $log = Join-Path $env:TEMP ('spack-windows-reset-{0}.log' -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
    $switches = @('-Apply', '-Force', '-RunInstallCleanup', '-KeepSpackConfig', '-CleanSpackCaches', '-IncludeWindowsKits')
    $values = @($Apply, $Force, $RunInstallCleanup, $KeepSpackConfig, $CleanSpackCaches, $IncludeWindowsKits)

    $inner = "& '$PSCommandPath'"
    for ($i = 0; $i -lt $switches.Count; $i++) {
        if ($values[$i]) { $inner += ' ' + $switches[$i] }
    }
    if ($SpackRoot) { $inner += " -SpackRoot '$SpackRoot'" }
    $inner += " *> '$log'; exit `$LASTEXITCODE"

    Write-Host "Relaunching elevated; output is captured in $log" -ForegroundColor Yellow
    try {
        $proc = Start-Process -FilePath 'powershell' -Verb RunAs -PassThru -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $inner)
    } catch {
        Write-Error "elevation failed: $($_.Exception.Message)"
        exit 2
    }

    # Tail the child's log while it runs; otherwise long uninstall steps look like a hang.
    $shown = 0
    while (-not $proc.HasExited) {
        Start-Sleep -Milliseconds 500
        $shown = Write-NewLogLines -Path $log -AlreadyShown $shown
    }
    $proc.WaitForExit()
    $shown = Write-NewLogLines -Path $log -AlreadyShown $shown
    if ($shown -eq 0) { Write-Warning "elevated run produced no log at $log" }
    exit $proc.ExitCode
}

if ($Elevate -and -not (Test-Elevated)) { Invoke-SelfElevate }

$spackCmd = Get-SpackCommand
$userConfigPath = Get-SpackUserConfigPath -SpackCmd $spackCmd

Write-Host ''
Write-Host '=== Spack Windows MSVC reset ===' -ForegroundColor Cyan
Write-Host ("  mode        : {0}" -f $(if ($Apply) { 'APPLY' } else { 'DRY RUN (pass -Apply to make changes)' }))
Write-Host ("  force       : {0}" -f $Force)
Write-Host ("  elevated    : {0}" -f (Test-Elevated))
Write-Host ("  spack       : {0}" -f $(if ($spackCmd) { $spackCmd } else { '<not found>' }))
Write-Host ("  user config : {0}" -f $userConfigPath)
Write-Host ''

if ($Apply -and -not (Test-Elevated)) {
    Write-Warning 'Not running elevated. Machine-wide uninstall, directory and registry steps will be skipped. Re-run with -Elevate or from an Administrator shell.'
}

Invoke-UninstallVsInstances
Invoke-InstallCleanup
Invoke-RemoveLeftoverDirectories
Invoke-RemoveInstallerMetadata
Invoke-RemoveStaleRegistryKeys
if (-not $KeepSpackConfig) {
    Invoke-CleanSpackConfig -SpackCmd $spackCmd -UserConfigPath $userConfigPath
} else {
    Add-Action -Step 'spack-config' -Item 'packages.yaml' -Status 'Skipped' -Detail '-KeepSpackConfig'
}
Invoke-CleanSpackStore -SpackCmd $spackCmd

Invoke-Verification -SpackCmd $spackCmd -UserConfigPath $userConfigPath

Write-Host ''
Write-Host '=== Actions ===' -ForegroundColor Cyan
$script:Actions | Format-Table -AutoSize -Wrap | Out-String -Width 200 | Write-Host

Write-Host '=== Verification ===' -ForegroundColor Cyan
$script:Checks | Format-Table -AutoSize -Wrap | Out-String -Width 200 | Write-Host

if ($IncludeWindowsKits) { Write-WindowsKitsReport }

$failed = @($script:Actions | Where-Object { $_.Status -eq 'Failed' })
$skipped = @($script:Actions | Where-Object { $_.Status -eq 'Skipped' })
$dirty = @($script:Checks | Where-Object { $_.Result -eq 'DIRTY' })

Write-Host ''
Write-Host '=== Summary ===' -ForegroundColor Cyan
Write-Host ("  actions failed  : {0}" -f $failed.Count)
Write-Host ("  actions skipped : {0}" -f $skipped.Count)
Write-Host ("  checks dirty    : {0}" -f $dirty.Count)

foreach ($item in $failed) { Write-Host ("  FAILED  {0}: {1} -- {2}" -f $item.Step, $item.Item, $item.Detail) -ForegroundColor Red }
foreach ($item in $skipped) { Write-Host ("  SKIPPED {0}: {1} -- {2}" -f $item.Step, $item.Item, $item.Detail) -ForegroundColor Yellow }
foreach ($item in $dirty) { Write-Host ("  DIRTY   {0} -- {1}" -f $item.Check, $item.Detail) -ForegroundColor Red }

if (-not $Apply) {
    Write-Host ''
    Write-Host 'DRY RUN: nothing was changed. Re-run elevated with -Apply -Force to clean the host.' -ForegroundColor Yellow
    exit 0
}

if ($failed.Count -eq 0 -and $dirty.Count -eq 0) {
    Write-Host ''
    Write-Host 'HOST IS CLEAN' -ForegroundColor Green
    exit 0
}

Write-Host ''
Write-Host 'HOST IS NOT CLEAN' -ForegroundColor Red
exit 1
