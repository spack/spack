##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

#
#
# This file is part of Spack and sets up the spack environment for zsh shells.
# This includes dotkit and module support as well as putting spack
# in your path.  Source it like this:
#
#    source /path/to/spack/share/spack/setup-env.zsh
#
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
# e.g., rather than requring a full spec for libelf, the user can type:
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
    _spack_subcommand=${1}; shift
    _spack_spec="$@"

    # Filter out use and unuse.  For any other commands, just run the
    # command.
    case ${_spack_subcommand} in
        "use"|"unuse")
            # Shift any other args for use off before parsing spec.
            _spack_use_args=""
            if [[ "$1" =~ ^- ]]; then
                _spack_use_args="$1"; shift
                _spack_spec="$@"
            fi

            # Here the user has run use or unuse with a spec.  Find a matching
            # spec with a dotkit using spack dotkit, then use or unuse the
            # result.  If spack dotkit comes back with an error, do nothing.
            if _spack_full_spec=$(command spack dotkit $_spack_spec); then
                $_spack_subcommand $_spack_use_args $_spack_full_spec
            fi
            return
            ;;
        "load"|"unload")
            # Shift any other args for module off before parsing spec.
            _spack_module_args=""
            if [[ "$1" =~ ^- ]]; then
                _spack_module_args="$1"; shift
                _spack_spec="$@"
            fi

            # Here the user has run use or unuse with a spec.  Find a matching
            # spec with a dotkit using spack dotkit, then use or unuse the
            # result.  If spack dotkit comes back with an error, do nothing.
            if _spack_full_spec=$(command spack tclmodule ${_spack_spec}); then
                module ${_spack_subcommand} ${_spack_module_args} ${_spack_full_spec}
            fi
            return
            ;;
        *)
            command spack $_spack_subcommand "$@"
            return
            ;;
    esac

    # If no args or -h, just run that command as well.
    if [ -z "$1" -o "$1" = "-h" ]; then
        command spack $_spack_subcommand -h
        return
    fi

}

#
# Set up dotkit and path in the user environment
#
_spack_share_dir="$(dirname $0:A)"
_spack_prefix="$(dirname $(dirname ${_spack_share_dir}))"

export DK_NODE="$_spack_share_dir/dotkit:$DK_NODE"
export MODULEPATH="$_spack_share_dir/modules:$MODULEPATH"
export PATH="$_spack_prefix/bin:$PATH"
