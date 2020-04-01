# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

########################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
########################################################################
# If no variable name is supplied, just append to PATH
# otherwise append to that variable.
set _pa_varname = PATH;
set _pa_new_path = $_pa_args[1];
[ $#_pa_args -gt 1 ] && set _pa_varname = $_pa_args[1] && set _pa_new_path = $_pa_args[2];

# Check whether the variable is set yet.
set _pa_old_value = ""
eval set _pa_set = '$?'$_pa_varname
[ $_pa_set -eq 1 ] && eval set _pa_old_value='$'$_pa_varname;

# Do the actual prepending here, if it is a dir and not already in the path
if ( -d $_pa_new_path && \:$_pa_old_value\: !~ *\:$_pa_new_path\:* ) then
    [ -n "$_pa_old_value" ] && setenv $_pa_varname $_pa_new_path\:$_pa_old_value
    [ -z "$_pa_old_value" ] && setenv $_pa_varname $_pa_new_path
endif

unset _pa_args _pa_new_path _pa_old_value _pa_set _pa_varname
