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
        setenv $varname $var$sep$value
        endif
    endif
    breaksw
case _spack_env_prepend:
    if ( ! $?varname || "$varname" == "" ) then
        setenv $varname $value
    else
        set var = `printenv $varname`
        setenv $varname $value$sep$var
        endif
    endif
    breaksw
case _spack_env_remove_value:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = $sep`printenv $varname`$sep
        set result = `echo $var | sed "s/$sep$value$sep/$sep/g" | rev | cut -c 2- | rev | cut -c 2-`
    endif

    setenv $varname $result
    breaksw
case _spack_env_remove_first:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = $sep`printenv $varname`$sep
        set result = `echo $var | sed "s/$sep$value$sep/$sep/" | rev | cut -c 2- | rev | cut -c 2-`
    endif

    setenv $varname $result
    breaksw
case _spack_env_remove_last:
    if ( ! $?varname || "$varname" == "") then
        set result = ""
    else
        set var = $sep`printenv $varname`$sep
        set result = `echo $var | sed "s/\(.*\)$sep$value$sep/\1$sep/" | rev | cut -c 2- | rev | cut -c 2-`
    endif

    setenv $varname $result
    breaksw
case _spack_env_prune_duplicates:
    # Only command that takes sep at position 3
    set sep = $value

    # This is heinous awk magic and I hate it...     for each field       print         if new       sep if not 1st field to print else ""
    set result = `printenv $varname | awk -F"$sep" '{for(i=1; i<=NF; i++) printf "%s", (\\!seen[$i]++? (i==1?"":FS) $i: "")}'`
    setenv $varname $result
    breaksw
endsw

unset command varname value sep var result
