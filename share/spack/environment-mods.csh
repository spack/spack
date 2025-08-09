# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


if ( $#argv < 2 || $#argv > 4 ) then
    echo "2-4 arguments are required"
    exit 1
endif

set command = $argv[1]
set varname = $argv[2]

if ( $#argv > 2 ) then
    set value = $argv[3]
endif
if ( $#argv == 4 ) then
    set sep = $argv[4]
endif

switch ($command)
case _spack_env_set:
    setenv $varname $value
    breaksw
case _spack_env_unset:
    unsetenv $varname
    breaksw
case _spack_env_append:
    if ( ! $?varname || "$varname" == "" ) then
        setenv $varname $value
    else
        set var = `printenv $varname`

        if ( ! ("$var" =~ *"$value"*) ) then
            set result = $var$sep$value
            setenv $varname $result
        endif
    endif
    breaksw
case _spack_env_prepend:
    if ( ! $?varname || "$varname" == "" ) then
        setenv $varname $value
    else
        set var = `printenv $varname`

        if ( ! ("$var" =~ *"$value"*) ) then
            set result = $value$sep$var
            setenv $varname $result
        endif
    endif
    breaksw
case _spack_env_remove_value:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = `printenv $varname`

        if ( "$var" == "$value" ) then
            set result = ""
        else if ( "$var" =~ "$value$sep"* ) then
            set result = `echo $var | sed "s#$value$sep##g"`
        else
            set result = `echo $var | sed "s#$sep$value##g"`
        endif
    endif

    setenv $varname $result
case _spack_env_remove_first:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = `printenv $varname`

        if ( "$var" == "$value" ) then
            set result = ""
        else if ( "$var" =~ "$value$sep"* ) then
            set result = `echo $var | sed "s#$value$sep##g"`
        else
            set result = `echo $var | sed "s#$sep$value##g"`
        endif
    endif

    setenv $varname $result
case _spack_env_remove_last:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = `printenv $varname`

        if ( "$var" == "$value" ) then
            set result = ""
        else
            echo "var: $var"
            echo "value: $value"
            set result = `echo $var | sed "s#\(.*\)$value#\1#"`
            echo $result
            # if ( "$var" =~ ^"$sep"* ) then: TODO: get the if working
            set result = `echo $result | sed "s#^$sep##1"`
            # else if ( "$var" =~ *"$sep" ) then
            set result = `echo $result | sed "s#\(.*\)$sep#\1#"`
            # else
            set result = `echo $result | sed "s#$sep$sep##g"`
            # endif
        endif
    endif

    setenv $varname $result
case _spack_env_prune_duplicates:
    # TODO: actually write this
    echo
endsw

unset command varname value sep var result
