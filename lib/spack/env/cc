#!/bin/bash
##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
    SPACK_DEBUG_LOG_ID
    SPACK_COMPILER_SPEC
    SPACK_CC_RPATH_ARG
    SPACK_CXX_RPATH_ARG
    SPACK_F77_RPATH_ARG
    SPACK_FC_RPATH_ARG
    SPACK_SHORT_SPEC
    SPACK_SYSTEM_DIRS
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

# test whether a path is a system directory
function system_dir {
    path="$1"
    for sd in ${SPACK_SYSTEM_DIRS[@]}; do
        if [ "${path}" == "${sd}" -o "${path}" == "${sd}/" ]; then
            # success if path starts with a system prefix
            return 0
        fi
    done
    return 1  # fail if path starts no system prefix
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
    ftn|f90|fc|f95|gfortran|flang|ifort|pgfortran|xlf90|xlf90_r|nagfor)
        command="$SPACK_FC"
        language="Fortran 90"
        comp="FC"
        lang_flags=F
        ;;
    f77|gfortran|flang|ifort|pgfortran|xlf|xlf_r|nagfor|ftn)
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
if [[ -z $mode ]] || [[ $mode == ld ]]; then
    for arg in "$@"; do
        case $arg in
            -v|-V|--version|-dumpversion)
                mode=vcheck
                break
                ;;
        esac
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

# Dump the mode and exit if the command is dump-mode.
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
if [[ ($mode == ld || $mode == ccld) && "$SPACK_SHORT_SPEC" =~ "darwin" ]];
then
    for arg in "$@"; do
        if [[ ($arg == -r && $mode == ld) ||
              ($arg == -r && $mode == ccld) ||
              ($arg == -Wl,-r && $mode == ccld) ]]; then
            add_rpaths=false
            break
        fi
    done
fi

# Save original command for debug logging
input_command="$@"
args=()

#
# Parse the command line arguments.
#
# We extract -L, -I, and -Wl,-rpath arguments from the command line and
# recombine them with Spack arguments later.  We parse these out so that
# we can make sure that system paths come last, that package arguments
# come first, and that Spack arguments are injected properly.
#
# All other arguments, including -l arguments, are treated as
# 'other_args' and left in their original order.  This ensures that
# --start-group, --end-group, and other order-sensitive flags continue to
# work as the caller expects.
#
# The libs variable is initialized here for completeness, and it is also
# used later to inject flags supplied via `ldlibs` on the command
# line. These come into the wrappers via SPACK_LDLIBS.
#
includes=()
libdirs=()
rpaths=()
system_includes=()
system_libdirs=()
system_rpaths=()
libs=()
other_args=()

while [ -n "$1" ]; do
    rp=""
    case "$1" in
        -I*)
            arg="${1#-I}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if system_dir "$arg"; then
                system_includes+=("$arg")
            else
                includes+=("$arg")
            fi
            ;;
        -L*)
            arg="${1#-L}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if system_dir "$arg"; then
                system_libdirs+=("$arg")
            else
                libdirs+=("$arg")
            fi
            ;;
        -l*)
            arg="${1#-l}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            other_args+=("-l$arg")
            ;;
        -Wl,*)
            arg="${1#-Wl,}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if [[ "$arg" = -rpath=* ]]; then
                rp="${arg#-rpath=}"
            elif [[ "$arg" = -rpath,* ]]; then
                rp="${arg#-rpath,}"
            elif [[ "$arg" = -rpath ]]; then
                shift; arg="$1"
                if [[ "$arg" != -Wl,* ]]; then
                    die "-Wl,-rpath was not followed by -Wl,*"
                fi
                rp="${arg#-Wl,}"
            else
                other_args+=("-Wl,$arg")
            fi
            ;;
        -Xlinker,*)
            arg="${1#-Xlinker,}"
            if [ -z "$arg" ]; then shift; arg="$1"; fi
            if [[ "$arg" = -rpath=* ]]; then
                rp="${arg#-rpath=}"
            elif [[ "$arg" = -rpath ]]; then
                shift; arg="$1"
                if [[ "$arg" != -Xlinker,* ]]; then
                    die "-Xlinker,-rpath was not followed by -Xlinker,*"
                fi
                rp="${arg#-Xlinker,}"
            else
                other_args+=("-Xlinker,$arg")
            fi
            ;;
        -Xlinker)
            if [[ "$2" == "-rpath" ]]; then
                if [[ "$3" != "-Xlinker" ]]; then
                    die "-Xlinker,-rpath was not followed by -Xlinker,*"
                fi
                shift 3;
                rp="$1"
            else
                other_args+=("$1")
            fi
            ;;
        *)
            other_args+=("$1")
            ;;
    esac

    # test rpaths against system directories in one place.
    if [ -n "$rp" ]; then
        if system_dir "$rp"; then
            system_rpaths+=("$rp")
        else
            rpaths+=("$rp")
        fi
    fi
    shift
done

#
# Prepend flags from Spack's cppflags, cflags, cxxflags, fcflags, fflags,
# and ldflags.
#

# Add ldflags
case "$mode" in
    ld|ccld)
        args=(${SPACK_LDFLAGS[@]} "${args[@]}") ;;
esac

# Add C, C++, and Fortran flags
case "$mode" in
    cc|ccld)
        case $lang_flags in
            C)
                args=(${SPACK_CFLAGS[@]} "${args[@]}") ;;
            CXX)
                args=(${SPACK_CXXFLAGS[@]} "${args[@]}") ;;
            F)
                args=(${SPACK_FFLAGS[@]} "${args[@]}") ;;
        esac
        ;;
esac

# Add cppflags
case "$mode" in
    cpp|as|cc|ccld)
        args=(${SPACK_CPPFLAGS[@]} "${args[@]}") ;;
esac

# Include all -L's and prefix/whatever dirs in rpath
case "$mode" in
    ld|ccld)
        $add_rpaths && rpaths+=("$SPACK_PREFIX/lib")
        $add_rpaths && rpaths+=("$SPACK_PREFIX/lib64")
        ;;
esac

# Read spack dependencies from the path environment variable
IFS=':' read -ra deps <<< "$SPACK_DEPENDENCIES"
for dep in "${deps[@]}"; do
    # Append include directories
    case "$mode" in
        cpp|cc|as|ccld)
            if [[ -d $dep/include ]]; then
                includes=("${includes[@]}" "$dep/include")
            fi
            ;;
    esac

    # Append lib/lib64 and RPATH directories
    case "$mode" in
        ld|ccld)
            if [[ -d $dep/lib ]]; then
                if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                    $add_rpaths && rpaths=("${rpaths[@]}" "$dep/lib")
                fi
                if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                    libdirs=("${libdirs[@]}" "$dep/lib")
                fi
            fi

            if [[ -d $dep/lib64 ]]; then
                if [[ $SPACK_RPATH_DEPS == *$dep* ]]; then
                    $add_rpaths && rpaths+=("$dep/lib64")
                fi
                if [[ $SPACK_LINK_DEPS == *$dep* ]]; then
                    libdirs+=("$dep/lib64")
                fi
            fi
            ;;
    esac
done

case "$mode" in
    ld|ccld)
        # Set extra RPATHs
        IFS=':' read -ra extra_rpaths <<< "$SPACK_COMPILER_EXTRA_RPATHS"
        for extra_rpath in "${extra_rpaths[@]}"; do
            $add_rpaths && rpaths+=("$extra_rpath")
            libdirs+=("$extra_rpath")
        done

        # Add SPACK_LDLIBS to args
        for lib in ${SPACK_LDLIBS[@]}; do
            libs+=("${lib#-l}")
        done
        ;;
esac

# Put the arguments back together in one list
# Includes and system includes first
for dir in "${includes[@]}";         do args+=("-I$dir"); done
for dir in "${system_includes[@]}";  do args+=("-I$dir"); done

# Library search paths
for dir in "${libdirs[@]}";          do args+=("-L$dir"); done
for dir in "${system_libdirs[@]}";   do args+=("-L$dir"); done

# RPATHs arguments
case "$mode" in
    ccld)
        for dir in "${rpaths[@]}";        do args+=("$rpath$dir"); done
        for dir in "${system_rpaths[@]}"; do args+=("$rpath$dir"); done
        ;;
    ld)
        for dir in "${rpaths[@]}";        do args+=("-rpath" "$dir"); done
        for dir in "${system_rpaths[@]}"; do args+=("-rpath" "$dir"); done
        ;;
esac

# Other arguments from the input command
args+=("${other_args[@]}")

# Inject SPACK_LDLIBS, if supplied
for lib in "${libs[@]}"; do
    args+=("-l$lib");
done

full_command=("$command")
full_command+=("${args[@]}")

# dump the full command if the caller supplies SPACK_TEST_COMMAND=dump-args
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
    input_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_DEBUG_LOG_ID.in.log"
    output_log="$SPACK_DEBUG_LOG_DIR/spack-cc-$SPACK_DEBUG_LOG_ID.out.log"
    echo "[$mode] $command $input_command" >> "$input_log"
    echo "[$mode] ${full_command[@]}" >> "$output_log"
fi

exec "${full_command[@]}"
