#----------------------------------*-sh-*--------------------------------------
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     |
#   \\  /    A nd           | Copyright (C) 2017 OpenCFD Ltd.
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# License
#     This file is part of OpenFOAM.
#
#     OpenFOAM is free software: you can redistribute it and/or modify it
#     under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
#     ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#     FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#     for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.
#
# Script
#     . change-userdir.sh PREFIX [SUFFIX]
#
#     Shortcuts (prefix)
#         -home           "$HOME/OpenFOAM/$USER-$WM_PROJECT_VERSION"
#         -none           remove from environment
#
#     Shortcuts (suffix)
#         -platforms      "platforms/$WM_OPTIONS"
#
# Description
#     Change WM_PROJECT_USER_DIR, FOAM_USER_APPBIN, FOAM_USER_LIBBIN
#     and the respective entries in PATH, LD_LIBRARY_PATH.
#     Also adjusts FOAM_RUN.
#
#     This can be useful with compiling additional OpenFOAM programs
#     (that use FOAM_USER_APPBIN, FOAM_USER_LIBBIN for their build),
#     to avoid conflicts with the normal user bin/lib files.
#
#     The suffix value should normally include "platforms/$WM_OPTIONS"
#
# Example
#     . /path/change-userdir.sh -home -platforms
#
#   corresponds to the standard user location:
#
#     $HOME/OpenFOAM/$USER-$WM_PROJECT_VERSION/platforms/$WM_OPTIONS
#
#------------------------------------------------------------------------------

if [ "$#" -ge 1 ]
then
    prefix="$1"
    suffix="$2"

    foamOldDirs="$FOAM_USER_APPBIN $FOAM_USER_LIBBIN"
    foamClean=$WM_PROJECT_DIR/bin/foamCleanPath
    if [ -x "$foamClean" ]
    then
        cleaned=$($foamClean "$PATH" "$foamOldDirs") && PATH="$cleaned"
        cleaned=$($foamClean "$LD_LIBRARY_PATH" "$foamOldDirs") \
            && LD_LIBRARY_PATH="$cleaned"
    fi

    case "$suffix" in
        -plat*) suffix="platforms/$WM_OPTIONS" ;;
    esac
    case "$prefix" in
        -home) prefix="$HOME/OpenFOAM/$USER-${WM_PROJECT_VERSION:-unknown}" ;;
        -none) unset prefix ;;
    esac

    if [ -n "$prefix" ]
    then
        export WM_PROJECT_USER_DIR="$prefix"
        export FOAM_RUN="$prefix/run"

        prefix="$prefix${suffix:+/}${suffix}"
        export FOAM_USER_APPBIN="$prefix/bin"
        export FOAM_USER_LIBBIN="$prefix/lib"

        PATH="$FOAM_USER_APPBIN:$PATH"
        LD_LIBRARY_PATH="$FOAM_USER_LIBBIN:$LD_LIBRARY_PATH"
    else
        unset WM_PROJECT_USER_DIR FOAM_RUN FOAM_USER_APPBIN FOAM_USER_LIBBIN
    fi
fi

unset foamClean foamOldDirs cleaned prefix suffix

#------------------------------------------------------------------------------
