# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

<#
.SYNOPSIS
    Install the minimal Visual Studio Build Tools components that Spack needs on Windows.

.DESCRIPTION
    Spack on Windows requires an MSVC C/C++ toolset, a Windows SDK (which also provides WGL),
    and the CMake/Ninja pair that ships with Visual Studio. This script installs exactly those
    components and nothing else -- no IDE workload, no ARM/ARM64 toolsets, no WDK. Because MSVC
    has no Fortran compiler, the Intel oneAPI Fortran compiler (ifx) is installed as well; pass
    -SkipFortran to leave it out.

    If a Visual Studio or Build Tools instance already exists, the missing components are added
    to it with the Visual Studio Installer. If no instance exists, Build Tools is installed with
    winget. Both paths are unattended and idempotent: re-running when everything is present is
    a no-op.

    The WDK is never installed, but an existing machine-wide WDK is registered as an external,
    because Spack cannot build one: the Windows Kits family is a single shared installation.

    After the toolchain is in place the script registers it with Spack ("spack compiler find",
    "spack external find"), then verifies the result by checking for the specific files Spack
    needs and reports anything missing.

    Optional diagnostic data collection is turned off by default: no optional components are
    requested, the VSCEIP OptIn registry value is set to 0, and VSCMD_SKIP_SENDTELEMETRY is set
    machine-wide so VsDevCmd.bat does not report developer-shell usage. Pass -KeepTelemetry to
    leave those settings untouched. Note that the MSVC telemetry helper VCTIP.EXE ships as part
    of the compiler toolset and cannot be deselected at install time.

.PARAMETER Apply
    Perform the installation. Without this switch the script only reports what it would do.

.PARAMETER Elevate
    Relaunch the script with an administrator token (UAC prompt) and stream the elevated run's
    output back to this console.

.PARAMETER Components
    Override the component IDs to install. Defaults to the MSVC x64/x86 toolset, a Windows 11
    SDK, and C++ CMake tools for Windows.

.PARAMETER WingetPackageId
    winget package used when no Visual Studio instance exists.
    Defaults to Microsoft.VisualStudio.2022.BuildTools.

.PARAMETER SkipFortran
    Do not install the Intel oneAPI Fortran compiler (ifx). MSVC provides no Fortran, so it is
    installed by default for packages that contain Fortran sources. It comes from winget, so no
    manual download is required; an already-downloaded offline installer is used only as a
    fallback when winget is unavailable.

.PARAMETER FortranInstaller
    Path to an Intel Fortran offline installer to use instead of winget. When omitted and
    winget is unavailable, the newest *fortran*offline*.exe in the Downloads folder is used.

.PARAMETER FortranWingetId
    winget package for the Intel Fortran compiler. Defaults to Intel.FortranCompiler.

.PARAMETER SkipSpackConfig
    Do not run "spack compiler find" / "spack external find" after installing.

.PARAMETER KeepTelemetry
    Leave the Visual Studio telemetry settings alone. By default this script opts out of the
    Customer Experience Improvement Program by setting the documented OptIn=0 registry values,
    because Build Tools installs have no UI for this, and sets VSCMD_SKIP_SENDTELEMETRY=1.
    Opting out needs elevation; without it the step is reported as skipped.

.PARAMETER SpackRoot
    Path to the Spack checkout. Defaults to the checkout containing this script.

.EXAMPLE
    .\share\spack\qa\windows_install_msvc.ps1
    Report what is missing and what would be installed, change nothing.

.EXAMPLE
    .\share\spack\qa\windows_install_msvc.ps1 -Apply -Elevate
    Prompt for elevation and install the missing components.

.LINK
    https://learn.microsoft.com/visualstudio/install/workload-component-id-vs-build-tools

.LINK
    https://learn.microsoft.com/visualstudio/ide/visual-studio-experience-improvement-program

.LINK
    https://github.com/oneapi-src/oneapi-ci/blob/master/scripts/install_windows.bat
#>

#Requires -Version 5.1

[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$Elevate,
    [string[]]$Components,
    [string]$WingetPackageId = 'Microsoft.VisualStudio.2022.BuildTools',
    [switch]$SkipFortran,
    [string]$FortranInstaller,
    [string]$FortranWingetId = 'Intel.FortranCompiler',
    [switch]$SkipSpackConfig,
    [switch]$KeepTelemetry,
    [string]$SpackRoot
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'

# Minimal component set. See the .LINK reference for the authoritative ID list.
#   VC.Tools.x86.x64      MSVC C/C++ build tools for x64/x86 (latest)
#   Windows11SDK.26100    Windows SDK; also supplies WGL (um\x64\OpenGL32.Lib) and the UCRT libs
#   VC.CMake.Project      "C++ CMake tools for Windows", which bundles CMake and Ninja
$DefaultComponents = @(
    'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
    'Microsoft.VisualStudio.Component.Windows11SDK.26100',
    'Microsoft.VisualStudio.Component.VC.CMake.Project'
)
if (-not $Components) { $Components = $DefaultComponents }

$script:Actions = New-Object System.Collections.ArrayList
$script:Checks = New-Object System.Collections.ArrayList

function Add-Action {
    param([string]$Step, [string]$Item, [string]$Status, [string]$Detail = '')
    $null = $script:Actions.Add([pscustomobject]@{
            Step = $Step; Item = $Item; Status = $Status; Detail = $Detail
        })
}

function Add-Check {
    param([string]$Check, [bool]$Passed, [string]$Detail = '')
    $null = $script:Checks.Add([pscustomobject]@{
            Check = $Check; Result = $(if ($Passed) { 'OK' } else { 'MISSING' }); Detail = $Detail
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

function Invoke-VsWhere {
    param([string[]]$ArgumentList)
    $installerDir = Get-VsInstallerDirectory
    if (-not $installerDir) { return @() }
    $vswhere = Join-Path $installerDir 'vswhere.exe'
    if (-not (Test-Path -LiteralPath $vswhere)) { return @() }

    $raw = & $vswhere @ArgumentList 2>&1
    if ($LASTEXITCODE -ne 0) { return @() }
    $text = ($raw | Out-String).Trim()
    if (-not $text) { return @() }
    try {
        $parsed = $text | ConvertFrom-Json
    } catch {
        return @()
    }
    if ($null -eq $parsed) { return @() }
    return @($parsed)
}

function Get-VsInstances {
    return Invoke-VsWhere -ArgumentList @('-all', '-prerelease', '-products', '*', '-format', 'json')
}

function Test-VsComponent {
    param([string]$ComponentId)
    # @() is required: PowerShell unrolls a single-element return value, and .Count on a bare
    # PSCustomObject is $null in Windows PowerShell 5.1.
    $found = @(Invoke-VsWhere -ArgumentList @(
            '-all', '-prerelease', '-products', '*', '-requires', $ComponentId, '-format', 'json'))
    return $found.Count -gt 0
}

function Write-Step {
    param([string]$Message)
    Write-Host "  -> $Message" -ForegroundColor DarkGray
}

function Invoke-Tool {
    param([string]$FilePath, [string[]]$ArgumentList, [switch]$Stream)

    # -Stream echoes each line as it arrives; installers can run for many minutes and are
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

function Get-InstallerLogHint {
    <# The VS bootstrapper and installer write dd_*.log files to %TEMP%. #>
    $logs = Get-ChildItem -LiteralPath $env:TEMP -Filter 'dd_*.log' -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 3
    if (-not $logs) { return "no dd_*.log found in $env:TEMP" }
    return ($logs | ForEach-Object { $_.FullName }) -join '; '
}

function Get-InstallerExitDetail {
    param([int]$ExitCode, [string]$Output)
    switch ($ExitCode) {
        0 { return 'installer reported success' }
        3010 { return 'installer reported success, reboot required' }
        1602 { return 'cancelled by the user (1602)' }
        1603 { return "fatal installer error (1603). Logs: $(Get-InstallerLogHint)" }
        default { return "exit $ExitCode. Logs: $(Get-InstallerLogHint). Output: $Output" }
    }
}

# Process names used by the Visual Studio Installer and its bootstrapper. Only one may run at a
# time; a second invocation fails without a distinguishing exit code.
$VsInstallerProcessNames = @(
    'vs_installer', 'vs_installershell', 'vs_installerservice', 'vs_bootstrapper',
    'vs_setup_bootstrapper', 'vs_buildtools', 'VSIXInstaller', 'setup'
)

function Get-RunningVsInstallerProcesses {
    return @(Get-Process -Name $VsInstallerProcessNames -ErrorAction SilentlyContinue)
}

function Confirm-ComponentsInstalled {
    param([string[]]$Expected, [int]$TimeoutSeconds = 1800)

    # The installer detaches, so poll vswhere rather than trusting the exit code: winget and the
    # VS bootstrapper can both exit 0 without having installed anything.
    $start = Get-Date
    $deadline = $start.AddSeconds($TimeoutSeconds)
    $nextHeartbeat = $start.AddSeconds(30)
    Write-Step 'waiting for the Visual Studio Installer to register the components'
    do {
        $stillMissing = @($Expected | Where-Object { -not (Test-VsComponent -ComponentId $_) })
        if ($stillMissing.Count -eq 0) {
            Add-Action -Step 'confirm' -Item 'components' -Status 'Ok' -Detail 'all requested components are now present'
            return
        }
        Start-Sleep -Seconds 5
        if ((Get-Date) -ge $nextHeartbeat) {
            Write-Step ('still waiting ({0:n0}s elapsed)' -f ((Get-Date) - $start).TotalSeconds)
            $nextHeartbeat = (Get-Date).AddSeconds(30)
        }
    } while ((Get-Date) -lt $deadline)

    Add-Action -Step 'confirm' -Item ($stillMissing -join ', ') -Status 'Failed' `
        -Detail "still not installed after the installer reported success. Logs: $(Get-InstallerLogHint)"
}

# ---------------------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------------------

function Get-MissingComponents {
    $missing = @()
    foreach ($component in $Components) {
        if (Test-VsComponent -ComponentId $component) {
            Add-Action -Step 'components' -Item $component -Status 'NotNeeded' -Detail 'already installed'
        } else {
            $missing += $component
        }
    }
    return $missing
}

function Invoke-ModifyExistingInstance {
    param([object]$Instance, [string[]]$MissingComponents)

    $label = "$($Instance.displayName) [$($Instance.installationPath)]"
    if (-not $Apply) {
        Add-Action -Step 'vs-modify' -Item $label -Status 'DryRun' `
            -Detail "would add: $($MissingComponents -join ', ')"
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step 'vs-modify' -Item $label -Status 'Skipped' -Detail 'needs elevation'
        return
    }

    $installerDir = Get-VsInstallerDirectory
    $vsInstaller = if ($installerDir) { Join-Path $installerDir 'vs_installer.exe' } else { $null }
    if (-not $vsInstaller -or -not (Test-Path -LiteralPath $vsInstaller)) {
        Add-Action -Step 'vs-modify' -Item $label -Status 'Failed' -Detail 'vs_installer.exe not found'
        return
    }

    $toolArgs = @('modify', '--installPath', $Instance.installationPath)
    foreach ($component in $MissingComponents) { $toolArgs += @('--add', $component) }
    # No --wait: setup.exe rejects it for some verbs (exit 87) and detaches anyway, so
    # Confirm-ComponentsInstalled polls vswhere for the result instead.
    $toolArgs += @('--passive', '--norestart')

    Write-Step "adding components to $($Instance.installationPath)"
    $result = Invoke-Tool -FilePath $vsInstaller -ArgumentList $toolArgs -Stream
    $detail = Get-InstallerExitDetail -ExitCode $result.ExitCode -Output $result.Output
    $status = if ($result.ExitCode -eq 0 -or $result.ExitCode -eq 3010) { 'Ok' } else { 'Failed' }
    Add-Action -Step 'vs-modify' -Item $label -Status $status -Detail $detail
}

function Invoke-InstallBuildTools {
    param([string[]]$MissingComponents)

    $overrideArgs = @('--passive', '--norestart', '--wait')
    foreach ($component in $MissingComponents) { $overrideArgs += @('--add', $component) }
    $override = $overrideArgs -join ' '

    if (-not $Apply) {
        Add-Action -Step 'winget-install' -Item $WingetPackageId -Status 'DryRun' -Detail $override
        return
    }
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        Add-Action -Step 'winget-install' -Item $WingetPackageId -Status 'Failed' `
            -Detail 'winget not found; install "App Installer" or run the Build Tools bootstrapper manually'
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step 'winget-install' -Item $WingetPackageId -Status 'Skipped' -Detail 'needs elevation'
        return
    }

    Write-Step "installing $WingetPackageId with winget (several GB, this takes a while)"
    $result = Invoke-Tool -Stream -FilePath $winget.Source -ArgumentList @(
        'install', '--id', $WingetPackageId, '--exact', '--source', 'winget',
        '--accept-package-agreements', '--accept-source-agreements', '--disable-interactivity',
        '--override', $override)
    $detail = Get-InstallerExitDetail -ExitCode $result.ExitCode -Output $result.Output
    $status = if ($result.ExitCode -eq 0 -or $result.ExitCode -eq 3010) { 'Ok' } else { 'Failed' }
    Add-Action -Step 'winget-install' -Item $WingetPackageId -Status $status -Detail $detail
}

# ---------------------------------------------------------------------------------------
# Intel Fortran (optional)
# ---------------------------------------------------------------------------------------

function Get-OneApiRoots {
    $roots = @()
    if ($env:ONEAPI_ROOT) { $roots += $env:ONEAPI_ROOT }
    foreach ($base in Get-ProgramFilesRoots) { $roots += (Join-Path $base 'Intel\oneAPI') }
    return @($roots | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -Unique)
}

function Find-IfxExecutable {
    foreach ($root in Get-OneApiRoots) {
        $found = @(Get-ChildItem -Path (Join-Path $root 'compiler\*\bin\ifx.exe') -ErrorAction SilentlyContinue |
                Sort-Object FullName -Descending)
        if ($found.Count -gt 0) { return $found[0].FullName }
    }
    return $null
}

function Find-FortranOfflineInstaller {
    if ($FortranInstaller) {
        if (Test-Path -LiteralPath $FortranInstaller) { return $FortranInstaller }
        Write-Warning "no installer at -FortranInstaller '$FortranInstaller'"
        return $null
    }
    $downloads = Join-Path $env:USERPROFILE 'Downloads'
    if (-not (Test-Path -LiteralPath $downloads)) { return $null }
    $candidates = @(Get-ChildItem -LiteralPath $downloads -Filter '*fortran*offline*.exe' -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending)
    if ($candidates.Count -eq 0) { return $null }
    return $candidates[0].FullName
}

function Install-FortranFromOfflineInstaller {
    param([string]$InstallerPath)

    # Sequence and arguments follow Intel's own CI scripts; see the oneapi-ci .LINK reference.
    $extractDir = Join-Path $env:TEMP ('oneapi-extract-{0}' -f (Get-Date -Format 'yyyyMMddHHmmss'))
    Write-Step "extracting $InstallerPath"
    $extract = Invoke-Tool -Stream -FilePath $InstallerPath -ArgumentList @(
        '-s', '-x', '-f', $extractDir, '--log', 'extract.log')
    $bootstrapper = Join-Path $extractDir 'bootstrapper.exe'
    if ($extract.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $bootstrapper)) {
        Add-Action -Step 'fortran' -Item $InstallerPath -Status 'Failed' `
            -Detail "extraction failed (exit $($extract.ExitCode)): $($extract.Output)"
        return
    }
    try {
        Write-Step 'running the Intel oneAPI bootstrapper'
        $result = Invoke-Tool -Stream -FilePath $bootstrapper -ArgumentList @(
            '-s', '--action', 'install', '--eula=accept',
            '-p=NEED_VS2017_INTEGRATION=0', '-p=NEED_VS2019_INTEGRATION=0',
            '-p=NEED_VS2022_INTEGRATION=0', "--log-dir=$extractDir")
        $status = if ($result.ExitCode -eq 0 -or $result.ExitCode -eq 3010) { 'Ok' } else { 'Failed' }
        Add-Action -Step 'fortran' -Item $InstallerPath -Status $status `
            -Detail "bootstrapper exit $($result.ExitCode). Logs: $extractDir"
    } finally {
        Remove-Item -LiteralPath $extractDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-InstallFortran {
    $ifx = Find-IfxExecutable
    if ($ifx) {
        Add-Action -Step 'fortran' -Item 'ifx' -Status 'NotNeeded' -Detail $ifx
        return
    }
    if (-not $Apply) {
        Add-Action -Step 'fortran' -Item $FortranWingetId -Status 'DryRun' -Detail 'would install Intel Fortran (ifx)'
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step 'fortran' -Item $FortranWingetId -Status 'Skipped' -Detail 'needs elevation'
        return
    }

    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Step "installing $FortranWingetId with winget (this takes a while)"
        $result = Invoke-Tool -Stream -FilePath $winget.Source -ArgumentList @(
            'install', '--id', $FortranWingetId, '--exact', '--source', 'winget',
            '--accept-package-agreements', '--accept-source-agreements', '--disable-interactivity')
        if ($result.ExitCode -eq 0 -or $result.ExitCode -eq 3010) {
            Add-Action -Step 'fortran' -Item $FortranWingetId -Status 'Ok' -Detail 'installed via winget'
            return
        }
        Add-Action -Step 'fortran' -Item $FortranWingetId -Status 'Failed' `
            -Detail "winget exit $($result.ExitCode): $($result.Output)"
    }

    $offline = Find-FortranOfflineInstaller
    if (-not $offline) {
        Add-Action -Step 'fortran' -Item 'offline installer' -Status 'Skipped' `
            -Detail 'winget unavailable or failed and no *fortran*offline*.exe found; pass -FortranInstaller'
        return
    }
    Install-FortranFromOfflineInstaller -InstallerPath $offline
}

# ---------------------------------------------------------------------------------------
# Telemetry opt-out
# ---------------------------------------------------------------------------------------

function Get-VsceipKeys {
    $keys = @('HKLM:\SOFTWARE\Policies\Microsoft\VisualStudio\SQM')
    foreach ($instance in @(Get-VsInstances)) {
        $major = ($instance.installationVersion -split '\.')[0]
        if (-not $major) { continue }
        $keys += if ([Environment]::Is64BitOperatingSystem) {
            "HKLM:\SOFTWARE\Wow6432Node\Microsoft\VSCommon\$major.0\SQM"
        } else {
            "HKLM:\SOFTWARE\Microsoft\VSCommon\$major.0\SQM"
        }
    }
    return @($keys | Select-Object -Unique)
}

function Invoke-DisableTelemetry {
    $keys = Get-VsceipKeys

    if (-not $Apply) {
        foreach ($key in $keys) {
            Add-Action -Step 'telemetry' -Item $key -Status 'DryRun' -Detail 'would set OptIn=0'
        }
        Add-Action -Step 'telemetry' -Item 'VSCMD_SKIP_SENDTELEMETRY' -Status 'DryRun' -Detail 'would set to 1 (machine)'
        return
    }
    if (-not (Test-Elevated)) {
        Add-Action -Step 'telemetry' -Item 'VSCEIP opt-out' -Status 'Skipped' -Detail 'needs elevation'
        return
    }
    foreach ($key in $keys) {
        try {
            if (-not (Test-Path -LiteralPath $key)) {
                New-Item -Path $key -Force -ErrorAction Stop | Out-Null
            }
            New-ItemProperty -LiteralPath $key -Name 'OptIn' -PropertyType DWord -Value 0 -Force -ErrorAction Stop | Out-Null
            Add-Action -Step 'telemetry' -Item "$key\OptIn" -Status 'Ok' -Detail 'set to 0 (opted out)'
        } catch {
            Add-Action -Step 'telemetry' -Item $key -Status 'Failed' -Detail $_.Exception.Message
        }
    }

    # VsDevCmd.bat sends developer-shell telemetry only while this variable is empty.
    $existing = [Environment]::GetEnvironmentVariable('VSCMD_SKIP_SENDTELEMETRY', 'Machine')
    if ($existing) {
        Add-Action -Step 'telemetry' -Item 'VSCMD_SKIP_SENDTELEMETRY' -Status 'NotNeeded' -Detail "already set to '$existing'"
        return
    }
    try {
        [Environment]::SetEnvironmentVariable('VSCMD_SKIP_SENDTELEMETRY', '1', 'Machine')
        Add-Action -Step 'telemetry' -Item 'VSCMD_SKIP_SENDTELEMETRY' -Status 'Ok' -Detail 'set to 1 (machine)'
    } catch {
        Add-Action -Step 'telemetry' -Item 'VSCMD_SKIP_SENDTELEMETRY' -Status 'Failed' -Detail $_.Exception.Message
    }
}

# ---------------------------------------------------------------------------------------
# Spack registration
# ---------------------------------------------------------------------------------------

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

function Test-MsvcFortranConfigured {
    param([string]$PackagesYaml)

    if (-not (Test-Path -LiteralPath $PackagesYaml)) { return $false }
    $inMsvc = $false
    foreach ($line in @(Get-Content -LiteralPath $PackagesYaml)) {
        if ($line -match '^\s{2}msvc:\s*$') { $inMsvc = $true; continue }
        if (-not $inMsvc) { continue }
        if ($line -match '^\s{0,2}\S') { break }
        if ($line -match '^\s+fortran:\s*\S') { return $true }
    }
    return $false
}

function Invoke-RegisterWithSpack {
    param([string]$SpackCmd)

    $commands = @(
        @{ Label = 'spack compiler find'; Args = @('compiler', 'find') },
        @{ Label = 'spack external find --not-buildable win-sdk wgl win-wdk'
            Args  = @('external', 'find', '--not-buildable', 'win-sdk', 'wgl', 'win-wdk')
        },
        @{ Label = 'spack external find cmake ninja'; Args = @('external', 'find', 'cmake', 'ninja') }
    )

    # The msvc package provides Fortran and records the ifx/ifort path it finds during
    # detection, but `spack compiler find` never refreshes an already-registered compiler.
    # An msvc entry detected before Fortran existed would keep concretizing without one.
    if (-not $SkipFortran -and $SpackCmd -and (Find-IfxExecutable)) {
        $packagesYaml = Join-Path (Get-SpackUserConfigPath -SpackCmd $SpackCmd) 'packages.yaml'
        if (-not (Test-MsvcFortranConfigured -PackagesYaml $packagesYaml)) {
            if (-not $Apply) {
                Add-Action -Step 'spack' -Item 'packages:msvc' -Status 'DryRun' `
                    -Detail 'would re-detect msvc so it picks up the Fortran compiler'
            } else {
                $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList @('config', 'rm', 'packages:msvc')
                $status = if ($result.ExitCode -eq 0) { 'Ok' } else { 'Failed' }
                Add-Action -Step 'spack' -Item 'packages:msvc' -Status $status `
                    -Detail 'removed for re-detection with the Fortran compiler'
            }
        }
    }

    foreach ($command in $commands) {
        if (-not $SpackCmd) {
            Add-Action -Step 'spack' -Item $command.Label -Status 'Skipped' -Detail 'spack not found; pass -SpackRoot'
            continue
        }
        if (-not $Apply) {
            Add-Action -Step 'spack' -Item $command.Label -Status 'DryRun' -Detail 'would register externals'
            continue
        }
        $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList $command.Args
        if ($result.ExitCode -eq 0) {
            Add-Action -Step 'spack' -Item $command.Label -Status 'Ok' -Detail 'registered'
        } else {
            Add-Action -Step 'spack' -Item $command.Label -Status 'Failed' `
                -Detail "exit $($result.ExitCode): $($result.Output)"
        }
    }
}

# ---------------------------------------------------------------------------------------
# Verification: check for the exact files Spack needs, not just registry/installer metadata
# ---------------------------------------------------------------------------------------

function Get-WindowsKitLibDirectories {
    $kitsRoot = Join-Path ${env:ProgramFiles(x86)} 'Windows Kits\10\Lib'
    if (-not (Test-Path -LiteralPath $kitsRoot)) { return @() }
    return @(Get-ChildItem -LiteralPath $kitsRoot -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^\d+\.\d+\.\d+\.\d+$' } |
            Sort-Object Name -Descending)
}

function Test-KitFile {
    param([string]$RelativePath)
    foreach ($version in Get-WindowsKitLibDirectories) {
        $candidate = Join-Path $version.FullName $RelativePath
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    return $null
}

function Invoke-Verification {
    param([string]$SpackCmd)

    $toolsetInstances = @(Invoke-VsWhere -ArgumentList @(
            '-products', '*', '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
            '-format', 'json'))
    Add-Check -Check 'Visual Studio instance with the MSVC x64/x86 toolset' `
        -Passed ($toolsetInstances.Count -gt 0) `
        -Detail $(if ($toolsetInstances.Count -gt 0) { ($toolsetInstances | ForEach-Object { $_.installationPath }) -join '; ' } else { 'none' })

    $clPaths = @()
    $cmakePaths = @()
    $ninjaPaths = @()
    foreach ($instance in $toolsetInstances) {
        $root = $instance.installationPath
        $clPaths += @(Get-ChildItem -Path (Join-Path $root 'VC\Tools\MSVC\*\bin\Hostx64\x64\cl.exe') -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty FullName)
        $cmake = Join-Path $root 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
        if (Test-Path -LiteralPath $cmake) { $cmakePaths += $cmake }
        $ninja = Join-Path $root 'Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe'
        if (Test-Path -LiteralPath $ninja) { $ninjaPaths += $ninja }
    }

    Add-Check -Check 'MSVC cl.exe (Hostx64\x64)' -Passed ($clPaths.Count -gt 0) `
        -Detail $(if ($clPaths.Count -gt 0) { $clPaths[0] } else { 'not found' })
    Add-Check -Check 'CMake bundled with Visual Studio' -Passed ($cmakePaths.Count -gt 0) `
        -Detail $(if ($cmakePaths.Count -gt 0) { $cmakePaths[0] } else { 'not found' })
    Add-Check -Check 'Ninja bundled with Visual Studio' -Passed ($ninjaPaths.Count -gt 0) `
        -Detail $(if ($ninjaPaths.Count -gt 0) { $ninjaPaths[0] } else { 'not found' })

    $ucrt = Test-KitFile -RelativePath 'ucrt\x64\libucrt.lib'
    Add-Check -Check 'Windows SDK UCRT libs (x64)' -Passed ([bool]$ucrt) `
        -Detail $(if ($ucrt) { $ucrt } else { 'no ucrt\x64\libucrt.lib under any Windows Kits\10\Lib version' })

    $wgl = Test-KitFile -RelativePath 'um\x64\OpenGL32.Lib'
    Add-Check -Check 'WGL (OpenGL32.Lib, x64)' -Passed ([bool]$wgl) `
        -Detail $(if ($wgl) { $wgl } else { 'no um\x64\OpenGL32.Lib under any Windows Kits\10\Lib version' })

    if ($SkipFortran) {
        Add-Check -Check 'Intel Fortran (ifx)' -Passed $true -Detail 'not requested (-SkipFortran)'
    } else {
        $ifx = Find-IfxExecutable
        Add-Check -Check 'Intel Fortran (ifx)' -Passed ([bool]$ifx) `
            -Detail $(if ($ifx) { $ifx } else { 'no compiler\*\bin\ifx.exe under any oneAPI root' })
    }

    if ($SpackCmd) {
        $result = Invoke-Spack -SpackCmd $SpackCmd -ArgumentList @(
            'python', '-c',
            'import spack.operating_systems.windows_os as w; print(len(w.WindowsOs().compiler_search_paths))')
        if ($result.ExitCode -ne 0) {
            Add-Check -Check 'Spack detects MSVC search paths' -Passed $false -Detail $result.Output
        } else {
            $line = ($result.Output -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 1).Trim()
            $count = 0
            [void][int]::TryParse($line, [ref]$count)
            Add-Check -Check 'Spack detects MSVC search paths' -Passed ($count -gt 0) -Detail "$line path(s)"
        }
    } else {
        Add-Check -Check 'Spack detects MSVC search paths' -Passed $false -Detail 'spack not found; pass -SpackRoot'
    }
}

# ---------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------

function Write-NewLogLines {
    param([string]$Path, [int]$AlreadyShown)

    if (-not (Test-Path -LiteralPath $Path)) { return $AlreadyShown }
    $lines = @(Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue)
    if ($lines.Count -le $AlreadyShown) { return $AlreadyShown }
    $lines[$AlreadyShown..($lines.Count - 1)] | ForEach-Object { Write-Host $_ }
    return $lines.Count
}

function Invoke-SelfElevate {
    $log = Join-Path $env:TEMP ('spack-windows-install-{0}.log' -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
    $inner = "& '$PSCommandPath'"
    if ($Apply) { $inner += ' -Apply' }
    if ($SkipSpackConfig) { $inner += ' -SkipSpackConfig' }
    if ($KeepTelemetry) { $inner += ' -KeepTelemetry' }
    if ($SkipFortran) { $inner += ' -SkipFortran' }
    if ($FortranInstaller) { $inner += " -FortranInstaller '$FortranInstaller'" }
    if ($PSBoundParameters.ContainsKey('FortranWingetId')) { $inner += " -FortranWingetId '$FortranWingetId'" }
    if ($SpackRoot) { $inner += " -SpackRoot '$SpackRoot'" }
    if ($PSBoundParameters.ContainsKey('WingetPackageId')) { $inner += " -WingetPackageId '$WingetPackageId'" }
    if ($PSBoundParameters.ContainsKey('Components')) {
        $quoted = ($Components | ForEach-Object { "'$_'" }) -join ','
        $inner += " -Components $quoted"
    }
    $inner += " *> '$log'; exit `$LASTEXITCODE"

    Write-Host "Relaunching elevated; output is captured in $log" -ForegroundColor Yellow
    try {
        $proc = Start-Process -FilePath 'powershell' -Verb RunAs -PassThru -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $inner)
    } catch {
        Write-Error "elevation failed: $($_.Exception.Message)"
        exit 2
    }

    # Tail the child's log while it runs; otherwise long installer steps look like a hang.
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

Write-Host ''
Write-Host '=== Spack Windows MSVC install ===' -ForegroundColor Cyan
Write-Host ("  mode     : {0}" -f $(if ($Apply) { 'APPLY' } else { 'DRY RUN (pass -Apply to install)' }))
Write-Host ("  elevated : {0}" -f (Test-Elevated))
Write-Host ("  spack    : {0}" -f $(if ($spackCmd) { $spackCmd } else { '<not found>' }))
Write-Host '  components:'
foreach ($component in $Components) { Write-Host "    $component" }
Write-Host ''

if ($Apply -and -not (Test-Elevated)) {
    Write-Warning 'Not running elevated. Installation steps will be skipped. Re-run with -Elevate or from an Administrator shell.'
}

$missing = @(Get-MissingComponents)
if ($missing.Count -eq 0) {
    Add-Action -Step 'install' -Item '(none)' -Status 'NotNeeded' -Detail 'all components already present'
} else {
    $busy = @(Get-RunningVsInstallerProcesses)
    if ($Apply -and $busy.Count -gt 0) {
        $names = ($busy | ForEach-Object { "$($_.ProcessName)($($_.Id))" }) -join ', '
        Add-Action -Step 'preflight' -Item 'Visual Studio Installer' -Status 'Failed' `
            -Detail "already running: $names. Close it and re-run; only one installer may run at a time."
    } else {
        $instances = @(Get-VsInstances)
        if ($instances.Count -gt 0) {
            Invoke-ModifyExistingInstance -Instance $instances[0] -MissingComponents $missing
        } else {
            Invoke-InstallBuildTools -MissingComponents $missing
        }
        if ($Apply) { Confirm-ComponentsInstalled -Expected $missing }
    }
}

$installFailed = @($script:Actions | Where-Object { $_.Status -eq 'Failed' }).Count -gt 0
if ($SkipFortran) {
    Add-Action -Step 'fortran' -Item 'Intel Fortran' -Status 'Skipped' -Detail '-SkipFortran'
} elseif (-not $installFailed) {
    Invoke-InstallFortran
}

$installFailed = @($script:Actions | Where-Object { $_.Status -eq 'Failed' }).Count -gt 0
if ($KeepTelemetry) {
    Add-Action -Step 'telemetry' -Item 'VSCEIP opt-out' -Status 'Skipped' -Detail '-KeepTelemetry'
} elseif (-not $installFailed) {
    Invoke-DisableTelemetry
}

if ($SkipSpackConfig) {
    Add-Action -Step 'spack' -Item 'compiler/external find' -Status 'Skipped' -Detail '-SkipSpackConfig'
} elseif ($installFailed) {
    Add-Action -Step 'spack' -Item 'compiler/external find' -Status 'Skipped' -Detail 'installation did not complete'
} else {
    Invoke-RegisterWithSpack -SpackCmd $spackCmd
}

Invoke-Verification -SpackCmd $spackCmd

Write-Host ''
Write-Host '=== Actions ===' -ForegroundColor Cyan
$script:Actions | Format-Table -AutoSize -Wrap | Out-String -Width 200 | Write-Host

Write-Host '=== Verification ===' -ForegroundColor Cyan
$script:Checks | Format-Table -AutoSize -Wrap | Out-String -Width 200 | Write-Host

$failed = @($script:Actions | Where-Object { $_.Status -eq 'Failed' })
$skipped = @($script:Actions | Where-Object { $_.Status -eq 'Skipped' })
$incomplete = @($script:Checks | Where-Object { $_.Result -eq 'MISSING' })

Write-Host '=== Summary ===' -ForegroundColor Cyan
Write-Host ("  actions failed  : {0}" -f $failed.Count)
Write-Host ("  actions skipped : {0}" -f $skipped.Count)
Write-Host ("  checks missing  : {0}" -f $incomplete.Count)

foreach ($item in $failed) { Write-Host ("  FAILED  {0}: {1} -- {2}" -f $item.Step, $item.Item, $item.Detail) -ForegroundColor Red }
foreach ($item in $skipped) { Write-Host ("  SKIPPED {0}: {1} -- {2}" -f $item.Step, $item.Item, $item.Detail) -ForegroundColor Yellow }
foreach ($item in $incomplete) { Write-Host ("  MISSING {0} -- {1}" -f $item.Check, $item.Detail) -ForegroundColor Red }

if (-not $Apply) {
    Write-Host ''
    Write-Host 'DRY RUN: nothing was installed. Re-run with -Apply -Elevate to install.' -ForegroundColor Yellow
    exit 0
}

if ($failed.Count -eq 0 -and $incomplete.Count -eq 0) {
    Write-Host ''
    Write-Host 'PREREQUISITES SATISFIED' -ForegroundColor Green
    exit 0
}

Write-Host ''
Write-Host 'PREREQUISITES NOT SATISFIED' -ForegroundColor Red
exit 1
