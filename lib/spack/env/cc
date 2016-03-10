#!/bin/bash
##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
# Spack compiler wrapper script.
#
# Compiler commands go through this compiler wrapper in Spack builds.
# The compiler wrapper is a thin layer around the standard compilers.
# It enables several key pieces of functionality:
#
# 1. It allows Spack to swap compilers into and out of builds easily.
# 2. It adds several options to the compile line so that spack
#    packages can find their dependencies at build time and run time:
#      -I           arguments for dependency /include directories.
#      -L           arguments for dependency /lib directories.
#      -Wl,-rpath   arguments for dependency /lib directories.
#

# This is the list of environment variables that need to be set before
# the script runs.  They are set by routines in spack.build_environment
# as part of spack.package.Package.do_install().
parameters="
SPACK_PREFIX
SPACK_ENV_PATH
SPACK_DEBUG_LOG_DIR
SPACK_COMPILER_SPEC
SPACK_SHORT_SPEC"

# The compiler input variables are checked for sanity later:
#   SPACK_CC, SPACK_CXX, SPACK_F77, SPACK_FC
# Debug flag is optional; set to true for debug logging:
#   SPACK_DEBUG
# Test command is used to unit test the compiler script.
#   SPACK_TEST_COMMAND
# Dependencies can be empty for pkgs with no deps:
#   SPACK_DEPENDENCIES

# die()
# Prints a message and exits with error 1.
function die {
    echo "$@"
    exit 1
}

for param in $parameters; do
    if [ -z "${!param}" ]; then
        die "Spack compiler must be run from spack!  Input $param was missing!"
    fi
done

#
# Figure out the type of compiler, the language, and the mode so that
# the compiler script knows what to do.
#
# Possible languages are C, C++, Fortran 77, and Fortran 90.
# 'command' is set based on the input command to $SPACK_[CC|CXX|F77|F90]
#
# 'mode' is set to one of:
#    cc      compile
#    ld      link
#    ccld    compile & link
#    cpp     preprocessor
#    vcheck  version check
#
command=$(basename "$0")
case "$command" in
    cc|c89|c99|gcc|clang|icc|pgcc|xlc)
        command="$SPACK_CC"
        language="C"
        ;;
    c++|CC|g++|clang++|icpc|pgc++|xlc++)
        command="$SPACK_CXX"
        language="C++"
        ;;
    f90|fc|f95|gfortran|ifort|pgfortran|xlf90|nagfor)
        command="$SPACK_FC"
        language="Fortran 90"
        ;;
    f77|gfortran|ifort|pgfortran|xlf|nagfor)
        command="$SPACK_F77"
        language="Fortran 77"
        ;;
    cpp)
        mode=cpp
        ;;
    ld)
        mode=ld
        ;;
    *)
        die "Unkown compiler: $command"
        ;;
esac

# If any of the arguments below is present then the mode is vcheck. In vcheck mode nothing is added in terms of extra search paths or libraries
if [ -z "$mode" ]; then
    for arg in "$@"; do
        if [ "$arg" = -v -o "$arg" = -V -o "$arg" = --version -o "$arg" = -dumpversion ]; then
            mode=vcheck
            break
    fi
    done
fi

# Finish setting up the mode.

if [ -z "$mode" ]; then
    mode=ccld
    for arg in "$@"; do
        if [ "$arg" = -E ]; then
            mode=cpp
            break
        elif [ "$arg" = -c ]; then
            mode=cc
            break
        fi
    done
fi

# Dump the version and exit if we're in testing mode.
if [ "$SPACK_TEST_COMMAND" = "dump-mode" ]; then
    echo "$mode"
    exit
fi

# Check that at least one of the real commands was actually selected,
# otherwise we don't know what to execute.
if [ -z "$command" ]; then
    die "ERROR: Compiler '$SPACK_COMPILER_SPEC' does not support compiling $language programs."
fi

# Save original command for debug logging
input_command="$@"

if [ "$mode" == vcheck ] ; then
    exec ${command} "$@"
fi

#
# Now do real parsing of the command line args, trying hard to keep
# non-rpath linker arguments in the proper order w.r.t. other command
# line arguments.  This is important for things like groups.
#
includes=()
libraries=()
libs=()
rpaths=()
other_args=()

while [ -n "$1" ]; do
    case "$1" in
        -I*)
            arg="${1#-I}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            includes+=("$arg")
            ;;
        -L*)
            arg="${1#-L}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            libraries+=("$arg")
            ;;
        -l*)
            arg="${1#-l}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            libs+=("$arg")
            ;;
        -Wl,*)
            arg="${1#-Wl,}"
            # TODO: Handle multiple -Wl, continuations of -Wl,-rpath
            if [[ $arg == -rpath=* ]]; then
                arg="${arg#-rpath=}"
                for rpath in ${arg//,/ }; do
                    rpaths+=("$rpath")
                done
            elif [[ $arg == -rpath,* ]]; then
                arg="${arg#-rpath,}"
                for rpath in ${arg//,/ }; do
                    rpaths+=("$rpath")
                done
            elif [[ $arg == -rpath ]]; then
                shift; arg="$1"
                if [[ $arg != '-Wl,'* ]]; then
                    die "-Wl,-rpath was not followed by -Wl,*"
                fi
                arg="${arg#-Wl,}"
                for rpath in ${arg//,/ }; do
                    rpaths+=("$rpath")
                done
            else
                other_args+=("-Wl,$arg")
            fi
            ;;
        -Xlinker)
            shift; arg="$1";
            if [[ $arg = -rpath=* ]]; then
                rpaths+=("${arg#-rpath=}")
            elif [[ $arg = -rpath ]]; then
                shift; arg="$1"
                if [[ $arg != -Xlinker ]]; then
                    die "-Xlinker -rpath was not followed by -Xlinker <arg>"
                fi
                shift; arg="$1"
                rpaths+=("$arg")
            else
                other_args+=("-Xlinker")
                other_args+=("$arg")
            fi
            ;;
        *)
            other_args+=("$1")
            ;;
    esac
    shift
done

# Dump parsed values for unit testing if asked for
if [ -n "$SPACK_TEST_COMMAND" ]; then
    IFS=$'\n'
    case "$SPACK_TEST_COMMAND" in
        dump-includes)   echo "${includes[*]}";;
        dump-libraries)  echo "${libraries[*]}";;
        dump-libs)       echo "${libs[*]}";;
        dump-rpaths)     echo "${rpaths[*]}";;
        dump-other-args) echo "${other_args[*]}";;
        dump-all)
            echo "INCLUDES:"
            echo "${includes[*]}"
            echo
            echo "LIBRARIES:"
            echo "${libraries[*]}"
            echo
            echo "LIBS:"
            echo "${libs[*]}"
            echo
            echo "RPATHS:"
            echo "${rpaths[*]}"
            echo
            echo "ARGS:"
            echo "${other_args[*]}"
            ;;
        *)
            echo "ERROR: Unknown test command"
            exit 1 ;;
    esac
    exit
fi

# Read spack dependencies from the path environment variable
IFS=':' read -ra deps <<< "$SPACK_DEPENDENCIES"
for dep in "${deps[@]}"; do
    if [ -d "$dep/include" ]; then
        includes+=("$dep/include")
    fi

    if [ -d "$dep/lib" ]; then
        libraries+=("$dep/lib")
        rpaths+=("$dep/lib")
    fi

    if [ -d "$dep/lib64" ]; then
        libraries+=("$dep/lib64")
        rpaths+=("$dep/lib64")
    fi
done

# Include all -L's and prefix/whatever dirs in rpath
for dir in "${libraries[@]}"; do
    [[ dir = $SPACK_INSTALL* ]] && rpaths+=("$dir")
done
rpaths+=("$SPACK_PREFIX/lib")
rpaths+=("$SPACK_PREFIX/lib64")

# Put the arguments together
args=()
for dir in "${includes[@]}";  do args+=("-I$dir"); done
args+=("${other_args[@]}")
for dir in "${libraries[@]}"; do args+=("-L$dir"); done
for lib in "${libs[@]}";      do args+=("-l$lib"); done

if [ "$mode" = ccld ]; then
    for dir in "${rpaths[@]}"; do
        args+=("-Wl,-rpath")
        args+=("-Wl,$dir");
    done
elif [ "$mode" = ld ]; then
    for dir in "${rpaths[@]}"; do
        args+=("-rpath")
        args+=("$dir");
    done
fi

#
# Unset pesky environment variables that could affect build sanity.
#
unset LD_LIBRARY_PATH
unset LD_RUN_PATH
unset DYLD_LIBRARY_PATH

#
# Filter '.' and Spack environment directories out of PATH so that
# this script doesn't just call itself
#
IFS=':' read -ra env_path <<< "$PATH"
IFS=':' read -ra spack_env_dirs <<< "$SPACK_ENV_PATH"
spack_env_dirs+=(".")
PATH=""
for dir in "${env_path[@]}"; do
    remove=""
    for rm_dir in "${spack_env_dirs[@]}"; do
        if [ "$dir" = "$rm_dir" ]; then remove=True; fi
    done
    if [ -z "$remove" ]; then
        if [ -z "$PATH" ]; then
            PATH="$dir"
        else
            PATH="$PATH:$dir"
        fi
    fi
done
export PATH

full_command=("$command")
full_command+=("${args[@]}")

#
# Write the input and output commands to debug logs if it's asked for.
#
if [ "$SPACK_DEBUG" = "TRUE" ]; then
    input_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_SHORT_SPEC.in.log"
    output_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_SHORT_SPEC.out.log"
    echo "$input_command"     >> $input_log
    echo "$mode       ${full_command[@]}" >> $output_log
fi

exec "${full_command[@]}"
