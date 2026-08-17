# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# For zsh compatibility: enable sh emulation mode to ensure word splitting
# and consistent behavior with bash/dash
if [ -n "${ZSH_VERSION:-}" ]; then
    emulate sh
fi

# _separator_exists sep
#
# Fails if separator argument was not supplied
_separator_exists() {
    if [ -z "$1" ]; then
        echo "Missing argument: separator"
        return 1
    fi
    return 0
}

# _spack_env_varname_is_empty varname
#
# Return whether the variable varname is unset or set to the empty string.
_spack_env_varname_is_empty() {
    varname="$1"

    eval "test -z \"\${${varname}:-}\""
}

# _spack_env_set varname value
#
# Set the varname variable to value.
_spack_env_set() {
    varname="$1"
    value="$2"

    export $varname="$value"
}

# _spack_env_unset varname
#
# Unset varname in the environment.
_spack_env_unset() {
    varname="$1"

    unset "$varname"
}

# _spack_env_append varname value sep
#
# Append value to the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_append() {
    varname="$1"
    value="$2"
    sep="$3"

   _separator_exists "$sep" || return

    if _spack_env_varname_is_empty "$varname"; then
        export $varname="$value"
    else
        eval "current=\"\${${varname}}\""
        export $varname="$current$sep$value"
    fi
}

# _spack_env_prepend varname value sep
#
# Prepend value to the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_prepend() { # if not exporting then use lowercase
    varname="$1"
    value="$2"
    sep="$3"

   _separator_exists "$sep" || return

   if _spack_env_varname_is_empty "$varname"; then
        export $varname="$value"
    else
        eval "current=\"\${${varname}}\""
        export $varname="$value$sep$current"
    fi
}

# _spack_env_remove_value varname value sep
#
# Remove value from the flag list in variable varname.
# The list in varname is separated by the sep character.

_spack_env_remove_value() {
    varname="$1"
    value="$2"
    sep="$3"

    _separator_exists "$sep" || return

    accumulator="$sep"
    original_ifs="$IFS"
    IFS="$sep"

    # Disable globbing to prevent * in paths from expanding
    set -f
    eval "varname_value=\"\${${varname}}\""
    for val in $varname_value; do
        if [ "$val" != "$value" ]; then
            accumulator="$accumulator$val$sep"
        fi
    done
    set +f

    export IFS="$original_ifs"

    accumulator="${accumulator#$sep}"
    accumulator="${accumulator%$sep}"
    export $varname="$accumulator"
}

# _spack_env_remove_first varname value sep
#
# Remove the first value from the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_remove_first() {
    varname="$1"
    value="$2"
    sep="$3"

    _separator_exists "$sep" || return

    accumulator="$sep"
    original_ifs="$IFS"
    IFS="$sep"

    done="no"

    # Disable globbing to prevent * in paths from expanding
    set -f
    eval "varname_value=\"\${${varname}}\""
    for val in $varname_value; do
         if [ "$val" != "$value" ] || [ "$done" = "yes" ]; then
            accumulator="$accumulator$val$sep"
        else
            done="yes"
        fi
    done
    set +f

    export IFS="$original_ifs"

    accumulator="${accumulator#$sep}"
    accumulator="${accumulator%$sep}"
    export $varname="$accumulator"
}

# _spack_env_remove_last varname value sep
#
# Remove the last value from the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_remove_last() {
    varname="$1"
    value="$2"
    sep="$3"

    _separator_exists "$sep" || return

    original_ifs="$IFS"
    IFS="$sep"

    done="no"

    # Disable globbing to prevent * in paths from expanding
    set -f
    # Reverse the list order
    eval "varname_value=\"\${${varname}}\""
    reversed="$sep"
    for val in $varname_value; do
        reversed="$sep$val$reversed"
    done
    reversed="${reversed#$sep}"
    reversed="${reversed%$sep}"

    # Remove the first appearance of $value in the reversed list
    # Put the entries back in in reverse order to get back original order
    accumulator="$sep"
    for val in $reversed; do
        if [ "$val" != "$value" ] || [ "$done" = "yes" ]; then
            accumulator="$sep$val$accumulator"
        else
            done="yes"
        fi
    done
    accumulator="${accumulator#$sep}"
    accumulator="${accumulator%$sep}"
    set +f

    export IFS="$original_ifs"
    export $varname="$accumulator"
}

# _spack_env_prune_duplicate varname sep
#
# Remove duplicate elements from the list in variable
# varname, preserving precedence.
#
# The list in varname is separated by the sep character.
_spack_env_prune_duplicates() {
    varname="$1"
    sep="$2"

    _separator_exists "$sep" || return

    # keep separate var names since we delegate to another method
    prune_accumulator="$sep"
    pre_prune_ifs="$IFS"
    IFS="$sep"

    # Disable globbing to prevent * in paths from expanding
    set -f
    eval "varname_value=\"\${${varname}}\""
    while [ "$varname_value" != "" ]; do
        # for-loop to get the first entry, then break
        for val in $varname_value; do
            prune_accumulator="$prune_accumulator$val$sep"
            IFS="$pre_prune_ifs"  # setting IFS to $sep breaks _spack_env_remove_value
            _spack_env_remove_value "$varname" "$val" "$sep"
            IFS="$sep"
            eval "varname_value=\"\${${varname}}\""
            break
        done
    done
    set +f

    prune_accumulator="${prune_accumulator#$sep}"
    prune_accumulator="${prune_accumulator%$sep}"

    export IFS="$pre_prune_ifs"
    export $varname="$prune_accumulator"
}
