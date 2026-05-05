# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# _separator_exists sep
#
# False if separator argument was not supplied
function _separator_exists {
    param([string]$sep)

    if ([string]::IsNullOrEmpty($sep)) {
        Write-Host "Missing argument: separator"
        return $false
    }
    return $true
}

# _spack_env_varname_is_empty varname
#
# Return whether the variable varname is unset or set to the empty string.
function _spack_env_varname_is_empty {
    param([string]$varname)

    $val = [Environment]::GetEnvironmentVariable($varname)
    return [string]::IsNullOrEmpty($val)
}

# _spack_env_set varname value
#
# Set the varname variable to value.
function _spack_env_set {
    param(
        [string]$varname,
        [string]$value
    )

    [Environment]::SetEnvironmentVariable($varname, $value)
}

# _spack_env_unset varname
#
# Unset varname in the environment.
function _spack_env_unset {
    param([string]$varname)

    [Environment]::SetEnvironmentVariable($varname, $null)
}

# _spack_env_append varname value sep
#
# Append value to the flag list in variable varname.
# The list in varname is separated by the sep character.
function _spack_env_append {
    param(
        [string]$varname,
        [string]$value,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    if (_spack_env_varname_is_empty $varname) {
        _spack_env_set $varname $value
    } else {
        $current = [Environment]::GetEnvironmentVariable($varname)
        _spack_env_set $varname "$current$sep$value"
    }
}

# _spack_env_prepend varname value sep
#
# Prepend value to the flag list in variable varname.
# The list in varname is separated by the sep character.
function _spack_env_prepend {
    param(
        [string]$varname,
        [string]$value,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    if (_spack_env_varname_is_empty $varname) {
        _spack_env_set $varname $value
    } else {
        $current = [Environment]::GetEnvironmentVariable($varname)
        _spack_env_set $varname "$value$sep$current"
    }
}

# _spack_env_remove_value varname value sep
#
# Remove all occurrences of value from the flag list in variable varname.
# The list in varname is separated by the sep character.
function _spack_env_remove_value {
    param(
        [string]$varname,
        [string]$value,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    $current = [Environment]::GetEnvironmentVariable($varname)
    if ([string]::IsNullOrEmpty($current)) { return }

    $parts = $current.Split([string[]]$sep, [System.StringSplitOptions]::None)
    
    # -cne is used for case-sensitive strict inequality to match bash
    $filtered = $parts | Where-Object { $_ -cne $value }
    $new_value = $filtered -join $sep

    _spack_env_set $varname $new_value
}

# _spack_env_remove_first varname value sep
#
# Remove the first value from the flag list in variable varname.
# The list in varname is separated by the sep character.
function _spack_env_remove_first {
    param(
        [string]$varname,
        [string]$value,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    $current = [Environment]::GetEnvironmentVariable($varname)
    if ([string]::IsNullOrEmpty($current)) { return }

    $parts = $current.Split([string[]]$sep, [System.StringSplitOptions]::None)
    $done = $false
    
    $filtered = foreach ($val in $parts) {
        if ($val -cne $value -or $done) {
            $val
        } else {
            $done = $true
        }
    }

    $new_value = $filtered -join $sep
    _spack_env_set $varname $new_value
}

# _spack_env_remove_last varname value sep
#
# Remove the last value from the flag list in variable varname.
# The list in varname is separated by the sep character.
function _spack_env_remove_last {
    param(
        [string]$varname,
        [string]$value,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    $current = [Environment]::GetEnvironmentVariable($varname)
    if ([string]::IsNullOrEmpty($current)) { return }

    $parts = $current.Split([string[]]$sep, [System.StringSplitOptions]::None)
    $lastIndex = [Array]::LastIndexOf($parts, $value)

    if ($lastIndex -ge 0) {
        $list = [System.Collections.Generic.List[string]]::new([string[]]$parts)
        $list.RemoveAt($lastIndex)
        $new_value = $list -join $sep
        _spack_env_set $varname $new_value
    }
}

# _spack_env_prune_duplicates varname sep
#
# Remove duplicate elements from the list in variable
# varname, preserving precedence.
#
# The list in varname is separated by the sep character.
function _spack_env_prune_duplicates {
    param(
        [string]$varname,
        [string]$sep
    )

    if (-not (_separator_exists $sep)) { return }

    $current = [Environment]::GetEnvironmentVariable($varname)
    if ([string]::IsNullOrEmpty($current)) { return }

    $parts = $current.Split([string[]]$sep, [System.StringSplitOptions]::None)
    
    $seen = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    
    $filtered = foreach ($val in $parts) {
        if ($seen.Add($val)) {
            $val
        }
    }

    $new_value = $filtered -join $sep
    _spack_env_set $varname $new_value
}
