# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


########################################################################
#
# This file is part of Spack and sets up the spack environment for
# bash and zsh.  This includes dotkit support, module support, and
# it also puts spack in your path.  The script also checks that
# at least module support exists, and provides suggestions if it
# doesn't. Source it like this:
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
    if [ -n "${ZSH_VERSION:-}" ]; then
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

    _sp_subcommand=""
    if [ -n "$1" ]; then
        _sp_subcommand="$1"
        shift
    fi
    _sp_spec=("$@")

    # Filter out use and unuse.  For any other commands, just run the
    # command.
    case $_sp_subcommand in
        "cd")
            _sp_arg=""
            if [ -n "$1" ]; then
                _sp_arg="$1"
                shift
            fi
            if [[ "$_sp_arg" = "-h" || "$_sp_arg" = "--help" ]]; then
                command spack cd -h
            else
                LOC="$(spack location $_sp_arg "$@")"
                if [[ -d "$LOC" ]] ; then
                    cd "$LOC"
                else
                    return 1
                fi
            fi
            return
            ;;
        "env")
            _sp_arg=""
            if [ -n "$1" ]; then
                _sp_arg="$1"
                shift
            fi

            if [[ "$_sp_arg" = "-h" || "$_sp_arg" = "--help" ]]; then
                command spack env -h
            else
                case $_sp_arg in
                    activate)
                        _a="$@"
                        if [ -z "$1" -o "${_a#*--sh}" != "$_a" -o "${_a#*--csh}" != "$_a" -o "${_a#*-h}" != "$_a" ]; then
                            # no args or args contain -h/--help, --sh, or --csh: just execute
                            command spack "${args[@]}"
                        else
                            # actual call to activate: source the output
                            eval $(command spack $_sp_flags env activate --sh "$@")
                        fi
                        ;;
                    deactivate)
                        if [ -n "$1" ]; then
                            # with args: execute the command
                            command spack "${args[@]}"
                        else
                            # no args: source the output.
                            eval $(command spack $_sp_flags env deactivate --sh)
                        fi
                        ;;
                    *)
                        command spack "${args[@]}"
                        ;;
                esac
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

            _sp_spec=("$@")

            # Here the user has run use or unuse with a spec.  Find a matching
            # spec using 'spack module find', then use the appropriate module
            # tool's commands to add/remove the result from the environment.
            # If spack module command comes back with an error, do nothing.
            case $_sp_subcommand in
                "use")
                    if _sp_full_spec=$(command spack $_sp_flags module dotkit find $_sp_subcommand_args "${_sp_spec[@]}"); then
                        use $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi ;;
                "unuse")
                    if _sp_full_spec=$(command spack $_sp_flags module dotkit find $_sp_subcommand_args "${_sp_spec[@]}"); then
                        unuse $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi ;;
                "load")
                    if _sp_full_spec=$(command spack $_sp_flags module tcl find $_sp_subcommand_args "${_sp_spec[@]}"); then
                        module load $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
                    fi ;;
                "unload")
                    if _sp_full_spec=$(command spack $_sp_flags module tcl find $_sp_subcommand_args "${_sp_spec[@]}"); then
                        module unload $_sp_module_args $_sp_full_spec
                    else
                        $(exit 1)
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

# Export spack function so it is available in subshells (only works with bash)
if [ -n "${BASH_VERSION:-}" ]; then
	export -f spack
fi

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
# Find root directory and add bin to path.
#
_sp_share_dir=$(cd "$(dirname $_sp_source_file)" && pwd)
_sp_prefix=$(cd "$(dirname $(dirname $_sp_share_dir))" && pwd)
_spack_pathadd PATH       "${_sp_prefix%/}/bin"
export SPACK_ROOT=${_sp_prefix}

#
# Determine which shell is being used
#
function _spack_determine_shell() {
    # This logic is derived from the cea-hpc/modules profile.sh example at
    # https://github.com/cea-hpc/modules/blob/master/init/profile.sh.in
    #
    # The objective is to correctly detect the shell type even when setup-env
    # is sourced within a script itself rather than a login terminal.
    if [ -n "${BASH:-}" ]; then
        echo ${BASH##*/}
    elif [ -n "${ZSH_NAME:-}" ]; then
        echo $ZSH_NAME
    else
        PS_FORMAT= ps -p $$ | tail -n 1 | awk '{print $4}' | sed 's/^-//' | xargs basename
    fi
}
export SPACK_SHELL=$(_spack_determine_shell)

#
# Check whether a function of the given name is defined
#
function _spack_fn_exists() {
	LANG= type $1 2>&1 | grep -q 'function'
}

need_module="no"
if ! _spack_fn_exists use && ! _spack_fn_exists module; then
	need_module="yes"
fi;


#
# make available environment-modules
#
if [ "${need_module}" = "yes" ]; then
    eval `spack --print-shell-vars sh,modules`

    # _sp_module_prefix is set by spack --print-sh-vars
    if [ "${_sp_module_prefix}" != "not_installed" ]; then
        # activate it!
        # environment-modules@4: has a bin directory inside its prefix
        MODULE_PREFIX_BIN="${_sp_module_prefix}/bin"
        if [ ! -d "${MODULE_PREFIX_BIN}" ]; then
            # environment-modules@3 has a nested bin directory
            MODULE_PREFIX_BIN="${_sp_module_prefix}/Modules/bin"
        fi
        export MODULE_PREFIX_BIN
        _spack_pathadd PATH "${MODULE_PREFIX_BIN}"
        module() { eval `${MODULE_PREFIX_BIN}/modulecmd ${SPACK_SHELL} $*`; }
    fi;
else
    eval `spack --print-shell-vars sh`
fi;

#
# set module system roots
#
_sp_multi_pathadd() {
    local IFS=':'
    if  [[ -n "${ZSH_VERSION:-}" ]]; then
        setopt sh_word_split
    fi
    for pth in "$2"; do
        _spack_pathadd "$1" "${pth}/${_sp_sys_type}"
    done
}
_sp_multi_pathadd MODULEPATH "$_sp_tcl_roots"
_sp_multi_pathadd DK_NODE "$_sp_dotkit_roots"

# Add programmable tab completion for Bash
#
if [ -n "${BASH_VERSION:-}" ]; then
    source $_sp_share_dir/spack-completion.bash
fi
