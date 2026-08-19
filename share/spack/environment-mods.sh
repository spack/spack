# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    eval "remaining=\"\${${varname}}\""
    accumulator=""

    while [ -n "$remaining" ]; do
        if [ "$remaining" = "${remaining#*$sep}" ]; then
            val="$remaining"
            remaining=""
        else
            val="${remaining%%$sep*}"
            remaining="${remaining#*$sep}"
        fi

        if [ "$val" != "$value" ]; then
            if [ -z "$accumulator" ]; then
                accumulator="$val"
            else
                accumulator="$accumulator$sep$val"
            fi
        fi
    done

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

    eval "remaining=\"\${${varname}}\""
    accumulator=""
    found="no"

    while [ -n "$remaining" ]; do
        if [ "$remaining" = "${remaining#*$sep}" ]; then
            val="$remaining"
            remaining=""
        else
            val="${remaining%%$sep*}"
            remaining="${remaining#*$sep}"
        fi

        if [ "$val" = "$value" ] && [ "$found" = "no" ]; then
            if [ ! -n "$remaining" ]; then
                accumulator="$remaining"
                break
            fi
        else
            if [ -z "$accumulator" ]; then
                accumulator="$val"
            else
                accumulator="$accumulator$sep$val"
            fi
        fi
    done

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

    eval "remaining=\"\${${varname}}\""

    omit_last_match=""
    accumulator=""

    while [ -n "$remaining" ]; do
        # Extract first element
        if [ "$remaining" = "${remaining#*$sep}" ]; then
            val="$remaining"
            remaining=""
        else
            val="${remaining%%$sep*}"
            remaining="${remaining#*$sep}"
        fi

        if [ "$val" = "$value" ]; then
            if [ -z "$accumulator" ]; then
                accumulator="$val"
            else
                omit_last_match="$accumulator"
                accumulator="$accumulator$sep$val"
            fi
        else
            if [ -z "$omit_last_match" ]; then
                omit_last_match="$val"
            else
                omit_last_match="$omit_last_match$sep$val"
            fi

            if [ -z "$accumulator" ]; then
                accumulator="$val"
            else
                accumulator="$accumulator$sep$val"
            fi
        fi
    done

    export $varname="$omit_last_match"
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

    eval "remaining=\"\${${varname}}\""
    accumulator=""
    seen="$sep"

    while [ -n "$remaining" ]; do
        # Extract first element
        if [ "$remaining" = "${remaining#*$sep}" ]; then
            val="$remaining"
            remaining=""
        else
            val="${remaining%%$sep*}"
            remaining="${remaining#*$sep}"
        fi

        # Check if we've seen this value before
        case "$seen" in
            *"$sep$val$sep"*)
                # Already seen, skip it
                ;;
            *)
                # New value, add it
                seen="$seen$val$sep"
                if [ -z "$accumulator" ]; then
                    accumulator="$val"
                else
                    accumulator="$accumulator$sep$val"
                fi
                ;;
        esac
    done

    export $varname="$accumulator"
}
