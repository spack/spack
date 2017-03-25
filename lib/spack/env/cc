#!/bin/bash
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

# This is an array of environment variables that need to be set before
# the script runs. They are set by routines in spack.build_environment
# as part of spack.package.Package.do_install().
parameters=(
    SPACK_PREFIX
    SPACK_ENV_PATH
    SPACK_DEBUG_LOG_DIR
    SPACK_COMPILER_SPEC
    SPACK_CC_RPATH_ARG
    SPACK_CXX_RPATH_ARG
    SPACK_F77_RPATH_ARG
    SPACK_FC_RPATH_ARG
    SPACK_SHORT_SPEC
)

# The compiler input variables are checked for sanity later:
#   SPACK_CC, SPACK_CXX, SPACK_F77, SPACK_FC
# The default compiler flags are passed from these variables:
#   SPACK_CFLAGS, SPACK_CXXFLAGS, SPACK_FCFLAGS, SPACK_FFLAGS,
#   SPACK_LDFLAGS, SPACK_LDLIBS
# Debug env var is optional; set to "TRUE" for debug logging:
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

for param in ${parameters[@]}; do
    if [[ -z ${!param} ]]; then
        die "Spack compiler must be run from Spack! Input '$param' is missing."
    fi
done

# Figure out the type of compiler, the language, and the mode so that
# the compiler script knows what to do.
#
# Possible languages are C, C++, Fortran 77, and Fortran 90.
# 'command' is set based on the input command to $SPACK_[CC|CXX|F77|F90]
#
# 'mode' is set to one of:
#    vcheck  version check
#    cpp     preprocess
#    cc      compile
#    as      assemble
#    ld      link
#    ccld    compile & link

command=$(basename "$0")
comp="CC"
case "$command" in
    cpp)
        mode=cpp
        ;;
    cc|c89|c99|gcc|clang|icc|pgcc|xlc|xlc_r)
        command="$SPACK_CC"
        language="C"
        comp="CC"
        lang_flags=C
        ;;
    c++|CC|g++|clang++|icpc|pgc++|xlc++|xlc++_r)
        command="$SPACK_CXX"
        language="C++"
        comp="CXX"
        lang_flags=CXX
        ;;
    ftn|f90|fc|f95|gfortran|ifort|pgfortran|xlf90|xlf90_r|nagfor)
        command="$SPACK_FC"
        language="Fortran 90"
        comp="FC"
        lang_flags=F
        ;;
    f77|gfortran|ifort|pgfortran|xlf|xlf_r|nagfor|ftn)
        command="$SPACK_F77"
        language="Fortran 77"
        comp="F77"
        lang_flags=F
        ;;
    ld)
        mode=ld
        ;;
    *)
        die "Unkown compiler: $command"
        ;;
esac

# If any of the arguments below are present, then the mode is vcheck.
# In vcheck mode, nothing is added in terms of extra search paths or
# libraries.
if [[ -z $mode ]]; then
    for arg in "$@"; do
        if [[ $arg == -v || $arg == -V || $arg == --version || $arg == -dumpversion ]]; then
            mode=vcheck
            break
        fi
    done
fi

# Finish setting up the mode.
if [[ -z $mode ]]; then
    mode=ccld
    for arg in "$@"; do
        if [[ $arg == -E ]]; then
            mode=cpp
            break
        elif [[ $arg == -S ]]; then
            mode=as
            break
        elif [[ $arg == -c ]]; then
            mode=cc
            break
        fi
    done
fi

# Set up rpath variable according to language.
eval rpath=\$SPACK_${comp}_RPATH_ARG

# Dump the version and exit if we're in testing mode.
if [[ $SPACK_TEST_COMMAND == dump-mode ]]; then
    echo "$mode"
    exit
fi

# Check that at least one of the real commands was actually selected,
# otherwise we don't know what to execute.
if [[ -z $command ]]; then
    die "ERROR: Compiler '$SPACK_COMPILER_SPEC' does not support compiling $language programs."
fi

#
# Set paths as defined in the 'environment' section of the compiler config
#   names are stored in SPACK_ENV_TO_SET
#   values are stored in SPACK_ENV_SET_<varname>
#
IFS=':' read -ra env_set_varnames <<< "$SPACK_ENV_TO_SET"
for varname in "${env_set_varnames[@]}"; do
    spack_varname="SPACK_ENV_SET_$varname"
    export $varname=${!spack_varname}
    unset $spack_varname
done

#
# Filter '.' and Spack environment directories out of PATH so that
# this script doesn't just call itself
#
IFS=':' read -ra env_path <<< "$PATH"
IFS=':' read -ra spack_env_dirs <<< "$SPACK_ENV_PATH"
spack_env_dirs+=("" ".")
PATH=""
for dir in "${env_path[@]}"; do
    addpath=true
    for env_dir in "${spack_env_dirs[@]}"; do
        if [[ $dir == $env_dir ]]; then
            addpath=false
            break
        fi
    done
    if $addpath; then
        PATH="${PATH:+$PATH:}$dir"
    fi
done
export PATH

if [[ $mode == vcheck ]]; then
    exec ${command} "$@"
fi

# Darwin's linker has a -r argument that merges object files together.
# It doesn't work with -rpath.
# This variable controls whether they are added.
add_rpaths=true
if [[ ($mode == ld || $mode == ccld) && "$SPACK_SHORT_SPEC" =~ "darwin" ]]; then
    for arg in "$@"; do
        if [[ ($arg == -r && $mode == ld) || ($arg == -Wl,-r && $mode == ccld) ]]; then
            add_rpaths=false
            break
        fi
    done
fi

# Save original command for debug logging
input_command="$@"
args=("$@")

# Prepend cppflags, cflags, cxxflags, fcflags, fflags, and ldflags

# Add ldflags
case "$mode" in
    ld|ccld)
        args=(${SPACK_LDFLAGS[@]} "${args[@]}") ;;
esac

# Add compiler flags.
case "$mode" in
    cc|ccld)
    # Add c, cxx, fc, and f flags
        case $lang_flags in
            C)
                args=(${SPACK_CFLAGS[@]} "${args[@]}") ;;
            CXX)
                args=(${SPACK_CXXFLAGS[@]} "${args[@]}") ;;
        esac
        ;;
esac

# Add cppflags
case "$mode" in
    cpp|as|cc|ccld)
        args=(${SPACK_CPPFLAGS[@]} "${args[@]}") ;;
esac

case "$mode" in cc|ccld)
        # Add fortran flags
        case $lang_flags in
            F)
                args=(${SPACK_FFLAGS[@]} "${args[@]}") ;;
        esac
        ;;
esac

# Read spack dependencies from the path environment variable
IFS=':' read -ra deps <<< "$SPACK_DEPENDENCIES"
for dep in "${deps[@]}"; do
    # Prepend include directories
    if [[ -d $dep/include ]]; then
        if [[ $mode == cpp || $mode == cc || $mode == as || $mode == ccld ]]; then
            args=("-I$dep/include" "${args[@]}")
        fi
    fi

    # Prepend lib and RPATH directories
    if [[ -d $dep/lib ]]; then
        if [[ $mode == ccld ]]; then
            if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                $add_rpaths && args=("$rpath$dep/lib" "${args[@]}")
            fi
            if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                args=("-L$dep/lib" "${args[@]}")
            fi
        elif [[ $mode == ld ]]; then
            if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                $add_rpaths && args=("-rpath" "$dep/lib" "${args[@]}")
            fi
            if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                args=("-L$dep/lib" "${args[@]}")
            fi
        fi
    fi

    # Prepend lib64 and RPATH directories
    if [[ -d $dep/lib64 ]]; then
        if [[ $mode == ccld ]]; then
            if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                $add_rpaths && args=("$rpath$dep/lib64" "${args[@]}")
            fi
            if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                args=("-L$dep/lib64" "${args[@]}")
            fi
        elif [[ $mode == ld ]]; then
            if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                $add_rpaths && args=("-rpath" "$dep/lib64" "${args[@]}")
            fi
            if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                args=("-L$dep/lib64" "${args[@]}")
            fi
        fi
    fi
done

# Include all -L's and prefix/whatever dirs in rpath
if [[ $mode == ccld ]]; then
    $add_rpaths && args=("$rpath$SPACK_PREFIX/lib64" "${args[@]}")
    $add_rpaths && args=("$rpath$SPACK_PREFIX/lib"   "${args[@]}")
elif [[ $mode == ld ]]; then
    $add_rpaths && args=("-rpath" "$SPACK_PREFIX/lib64" "${args[@]}")
    $add_rpaths && args=("-rpath" "$SPACK_PREFIX/lib"   "${args[@]}")
fi

# Set extra RPATHs
IFS=':' read -ra extra_rpaths <<< "$SPACK_COMPILER_EXTRA_RPATHS"
for extra_rpath in "${extra_rpaths[@]}"; do
    if [[ $mode == ccld ]]; then
        $add_rpaths && args=("$rpath$extra_rpath" "${args[@]}")
    elif [[ $mode == ld ]]; then
        $add_rpaths && args=("-rpath" "$extra_rpath" "${args[@]}")
    fi
done

# Add SPACK_LDLIBS to args
case "$mode" in
    ld|ccld)
        args=("${args[@]}" ${SPACK_LDLIBS[@]}) ;;
esac

full_command=("$command" "${args[@]}")

# In test command mode, write out full command for Spack tests.
if [[ $SPACK_TEST_COMMAND == dump-args ]]; then
    echo "${full_command[@]}"
    exit
elif [[ -n $SPACK_TEST_COMMAND ]]; then
    die "ERROR: Unknown test command"
fi

#
# Write the input and output commands to debug logs if it's asked for.
#
if [[ $SPACK_DEBUG == TRUE ]]; then
    input_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_SHORT_SPEC.in.log"
    output_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_SHORT_SPEC.out.log"
    echo "[$mode] $command $input_command" >> "$input_log"
    echo "[$mode] ${full_command[@]}" >> "$output_log"
fi

exec "${full_command[@]}"
