##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

########################################################################
#
# This file is part of Spack and sets up the spack environment for
# bash and zsh.  This includes dotkit support, module support, and
# it also puts spack in your path.  Source it like this:
#
#    . /path/to/spack/share/spack/setup-env.sh
#
########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack use' and 'spack unuse' to shell functions.  This in turn
# allows them to be used to invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its
# arguments into a unique spack spec that is then passed to dotkit
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack dotfiles.
########################################################################

function spack {
    # Zsh does not do word splitting by default, this enables it for this function only
    if [ -n "$ZSH_VERSION" ]; then
        emulate -L sh
    fi

    # save raw arguments into an array before butchering them
    args=( "$@" )

    # accumulate initial flags for main spack command
    _sp_flags=""
    while [[ "$1" =~ ^- ]]; do
        _sp_flags="$_sp_flags $1"
        shift
    done

    # h and V flags don't require further output parsing.
    if [[ (! -z "$_sp_flags") && ("$_sp_flags" =~ '.*h.*' || "$_sp_flags" =~ '.*V.*') ]]; then
        command spack $_sp_flags "$@"
        return
    fi

    _sp_subcommand=$1; shift
    _sp_spec="$@"

    # Filter out use and unuse.  For any other commands, just run the
    # command.
    case $_sp_subcommand in
        "cd")
            _sp_arg="$1"; shift
            if [ "$_sp_arg" = "-h" ]; then
                command spack cd -h
            else
                LOC="$(spack location $_sp_arg "$@")"
                if [[ -d "$LOC" ]] ; then
                    cd "$LOC"
                fi
            fi
            return
            ;;
        "use"|"unuse"|"load"|"unload")
            # Shift any other args for use off before parsing spec.
            _sp_subcommand_args=""
            _sp_module_args=""
            while [[ "$1" =~ ^- ]]; do
                if [ "$1" = "-r" -o "$1" = "--dependencies" ]; then
                    _sp_subcommand_args="$_sp_subcommand_args $1"
                else
                    _sp_module_args="$_sp_module_args $1"
                fi
                shift
            done

            _sp_spec="$@"

            # Here the user has run use or unuse with a spec.  Find a matching
            # spec using 'spack module find', then use the appropriate module
            # tool's commands to add/remove the result from the environment.
            # If spack module command comes back with an error, do nothing.
            case $_sp_subcommand in
                "use")
                    if _sp_full_spec=$(command spack $_sp_flags module loads --input-only $_sp_subcommand_args --module-type dotkit $_sp_spec); then
                        use $_sp_module_args $_sp_full_spec
                    fi ;;
                "unuse")
                    if _sp_full_spec=$(command spack $_sp_flags module loads --input-only $_sp_subcommand_args --module-type dotkit $_sp_spec); then
                        unuse $_sp_module_args $_sp_full_spec
                    fi ;;
                "load")
                    if _sp_full_spec=$(command spack $_sp_flags module loads --input-only $_sp_subcommand_args --module-type tcl $_sp_spec); then
                        module load $_sp_module_args $_sp_full_spec
                    fi ;;
                "unload")
                    if _sp_full_spec=$(command spack $_sp_flags module loads --input-only $_sp_subcommand_args --module-type tcl $_sp_spec); then
                        module unload $_sp_module_args $_sp_full_spec
                    fi ;;
            esac
            ;;
        *)
            command spack "${args[@]}"
            ;;
    esac
}

########################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
########################################################################
function _spack_pathadd {
    # If no variable name is supplied, just append to PATH
    # otherwise append to that variable.
    _pa_varname=PATH
    _pa_new_path="$1"
    if [ -n "$2" ]; then
        _pa_varname="$1"
        _pa_new_path="$2"
    fi

    # Do the actual prepending here.
    eval "_pa_oldvalue=\${${_pa_varname}:-}"

    if [ -d "$_pa_new_path" ] && [[ ":$_pa_oldvalue:" != *":$_pa_new_path:"* ]]; then
        if [ -n "$_pa_oldvalue" ]; then
            eval "export $_pa_varname=\"$_pa_new_path:$_pa_oldvalue\""
        else
            export $_pa_varname="$_pa_new_path"
        fi
    fi
}

#
# Figure out where this file is.  Below code needs to be portable to
# bash and zsh.
#
_sp_source_file="${BASH_SOURCE[0]}"  # Bash's location of last sourced file.
if [ -z "$_sp_source_file" ]; then
    _sp_source_file="$0:A"           # zsh way to do it
    if [[ "$_sp_source_file" == *":A" ]]; then
        # Not zsh either... bail out with plain old $0,
        # which WILL NOT work if this is sourced indirectly.
        _sp_source_file="$0"
    fi
fi

#
# Set up modules and dotkit search paths in the user environment
#
_sp_share_dir=$(cd "$(dirname $_sp_source_file)" && pwd)
_sp_prefix=$(cd "$(dirname $(dirname $_sp_share_dir))" && pwd)
_spack_pathadd PATH       "${_sp_prefix%/}/bin"

_sp_sys_type=$(spack-python -c 'print(spack.architecture.sys_type())')
_sp_dotkit_root=$(spack-python -c "print(spack.util.path.canonicalize_path(spack.config.get_config('config').get('module_roots', {}).get('dotkit')))")
_sp_tcl_root=$(spack-python -c "print(spack.util.path.canonicalize_path(spack.config.get_config('config').get('module_roots', {}).get('tcl')))")
_spack_pathadd DK_NODE    "${_sp_dotkit_root%/}/$_sp_sys_type"
_spack_pathadd MODULEPATH "${_sp_tcl_root%/}/$_sp_sys_type"
