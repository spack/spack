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
#     . change-sitedir.sh PREFIX [SUFFIX]
#
#     Shortcuts (prefix)
#         -prefix         "$WM_PROJECT_INST_DIR/site"
#         -project        "$WM_PROJECT_DIR/site"
#         -none           remove from environment
#
#     Shortcuts (suffix)
#         -platforms      "platforms/$WM_OPTIONS"
#
# Description
#     Change WM_PROJECT_SITE, FOAM_SITE_APPBIN, FOAM_SITE_LIBBIN
#     and the respective entries in PATH, LD_LIBRARY_PATH.
#
#     This can be useful when temporarily reassigning the site directory
#     when packaging OpenFOAM.
#
#     The suffix value should normally include "platforms/$WM_OPTIONS"
#
# Example
#     . /path/change-sitedir.sh -prefix -platforms
#
#   corresponds to the standard site location:
#
#     $WM_PROJECT_INST_DIR/site{/$WM_PROJECT_VERSION/platforms/$WM_OPTIONS}
#
#------------------------------------------------------------------------------

if [ "$#" -ge 1 ]
then
    prefix="$1"
    suffix="$2"

    foamOldDirs="$FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN \
        $WM_PROJECT_SITE $WM_PROJECT_INST_DIR/site $WM_PROJECT_DIR/site"
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
        -prefix)  prefix="$WM_PROJECT_INST_DIR/site" ;;
        -project) prefix="$WM_PROJECT_DIR/site" ;;
        -none)    unset prefix ;;
    esac

    if [ -n "$prefix" ]
    then
        export WM_PROJECT_SITE="$prefix"

        prefix="$prefix/${WM_PROJECT_VERSION:-unknown}${suffix:+/}${suffix}"

        export FOAM_SITE_APPBIN="$prefix/bin"
        export FOAM_SITE_LIBBIN="$prefix/lib"
        PATH="$FOAM_SITE_APPBIN:$PATH"
        LD_LIBRARY_PATH="$FOAM_SITE_LIBBIN:$LD_LIBRARY_PATH"
    else
        unset WM_PROJECT_SITE FOAM_SITE_APPBIN FOAM_SITE_LIBBIN
    fi
fi

unset foamClean foamOldDirs cleaned prefix suffix

#------------------------------------------------------------------------------
