# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#!/bin/sh

# _separator_exists sep
#
# Fails if separator argument was not supplied
_separator_exists() {
    if [ -z "$1" ]; then
        echo "Missing argument: separator"
        exit 1
    fi
}

# _value_in_varname varname value sep
#
# Return whether the variable value is found in varname
_value_in_varname () {
    varname="$1"
    value="$2"

    eval "var=\"\${${varname}}\""

    test "${var#*$value}" != "$var"
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

   _separator_exists $sep

    if _spack_env_varname_is_empty "$varname"; then
        result=$value
    else
        eval "result=\"\${${varname}}\""

        if ! _value_in_varname "$varname" "$value"; then
            result=$result$sep$value
        fi
    fi

    export $varname=$result
}

# _spack_env_prepend varname value sep
#
# Prepend value to the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_prepend() { # if not exporting then use lowercase
    varname="$1"
    value="$2"
    sep="$3"

   _separator_exists $sep

   if _spack_env_varname_is_empty "$varname"; then
        result=$value
    else
        eval "result=\"\${${varname:-}}\""

        if ! _value_in_varname "$varname" "$value"; then
            result=$value$sep$result
        fi
    fi

    export $varname=$result
}

# _spack_env_remove_value varname value sep
#
# Remove value from the flag list in variable varname.
# The list in varname is separated by the sep character.

_spack_env_remove_value() {
    varname="$1"
    value="$2"
    sep="$3"

    _separator_exists $sep

    eval "varname_value=\"\${${varname}}\""

    if [ "$varname_value" == "$value" ]; then
        result=""
    elif [ "${varname_value##$value$sep}" != "${varname_value}" ]; then
        result=${varname_value##$value$sep}
    elif [ "${varname_value%%$sep$value}" != "${varname_value}" ]; then
        result=${varname_value%%$sep$value}
    else
        result=${varname_value[@]/$value$sep/}
    fi

    export $varname=$result
}

# _spack_env_remove_first varname value sep
#
# Remove the first value from the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_remove_first() {
    varname="$1"
    value="$2"
    sep="$3"

   _separator_exists $sep

    eval "varname_value=\"\${${varname}}\""

    if [ "$varname_value" == "$value" ]; then
        result=""
    elif [ "${varname_value##$value$sep}" != "${varname_value}" ]; then
        result=${varname_value##$value$sep}
    elif [ "${varname_value[@]/$value$sep/}" != "${varname_value}" ]; then
        result=${varname_value[@]/$value$sep/}
    else
        result=${varname_value%%$sep$value}
    fi

    export $varname=$result
}

# _spack_env_remove_last varname value sep
#
# Remove the last value from the flag list in variable varname.
# The list in varname is separated by the sep character.
_spack_env_remove_last() {
    varname="$1"
    value="$2"
    sep="$3"

   _separator_exists $sep

    eval "varname_value=\"\${${varname}}\""

    if [ "$varname_value" == "$value" ]; then
        result=""
    elif [ "${varname_value%%$sep$value}" != "${varname_value}" ]; then
        result=${varname_value%%$sep$value}
    elif [ "${varname_value[@]/$value$sep/}" != "${varname_value}" ]; then
        result=${varname_value[@]/$value$sep/}
    else
        result=${varname_value##$value$sep}
    fi

    export $varname=$result
}

# _spack_env_prune_duplicate varname sep
#
# Remove duplicate elements from the list in variable
# varname, preserving precedence.
#
# The list in varname is separated by the sep character.
_spack_env_prune_duplicates() {
    # TODO: actually write this
    echo
}
