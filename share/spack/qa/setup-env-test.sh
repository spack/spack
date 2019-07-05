#!/bin/sh
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This script tests that Spack's setup-env.sh init script works.
#
# The tests are portable to bash, zsh, and bourne shell, and can be run
# in any of these shells.
#

# ------------------------------------------------------------------------
# Functions for color output.
# ------------------------------------------------------------------------

# Colors for output
red='\033[1;31m'
cyan='\033[1;36m'
green='\033[1;32m'
reset='\033[0m'

echo_red() {
    printf "${red}$*${reset}\n"
}

echo_green() {
    printf "${green}$*${reset}\n"
}

echo_msg() {
    printf "${cyan}$*${reset}\n"
}

# ------------------------------------------------------------------------
# Generic functions for testing shell code.
# ------------------------------------------------------------------------

# counts of test successes and failures.
success=0
errors=0

# Print out a header for a group of tests.
title() {
    echo
    echo_msg "$@"
    echo_msg "---------------------------------"
}

# echo FAIL in red text; increment failures
fail() {
    echo_red FAIL
    errors=$((errors+1))
}

#
# Echo SUCCESS in green; increment successes
#
pass() {
    echo_green SUCCESS
    success=$((success+1))
}

#
# Run a command and suppress output unless it fails.
# On failure, echo the exit code and output.
#
succeeds() {
    printf "'%s' succeeds ... " "$*"
    output=$($* 2>&1)
    err="$?"

    if [ "$err" != 0 ]; then
        fail
        echo_red "Command failed with error $err."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Run a command and suppress output unless it succeeds.
# If the command succeeds, echo the output.
#
fails() {
    printf "'%s' fails ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "$err" = 0 ]; then
        fail
        echo_red "Command failed with error $err."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Ensure that a string is in the output of a command.
# Suppresses output on success.
# On failure, echo the exit code and output.
#
contains() {
    string="$1"
    shift

    printf "'%s' output contains '$string' ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "${output#*$string}" = "${output}" ]; then
        fail
        echo_red "Command exited with error $err."
        echo_red "'$string' was not in output."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Ensure that a variable is set.
#
is_set() {
    printf "'%s' is set ... " "$1"
    if eval "[ -z \${${1:-}+x} ]"; then
        fail
        echo_msg "$1 was not set!"
    else
        pass
    fi
}

#
# Ensure that a variable is not set.
# Fails and prints the value of the variable if it is set.
#
is_not_set() {
    printf "'%s' is not set ... " "$1"
    if eval "[ ! -z \${${1:-}+x} ]"; then
        fail
        echo_msg "$1 was set:"
        echo "    $1"
    else
        pass
    fi
}


# -----------------------------------------------------------------------
# Instead of invoking the module/use/dotkit commands, we print the
# arguments that Spack invokes the command with, so we can check that
# Spack passes the expected arguments in the tests below.
#
# We make that happen by defining the sh functions below.
# -----------------------------------------------------------------------
module() {
    echo module "$@"
}

use() {
    echo use "$@"
}

unuse() {
    echo unuse "$@"
}

# -----------------------------------------------------------------------
# Setup test environment and do some preliminary checks
# -----------------------------------------------------------------------

# Make sure no environment is active
unset SPACK_ENV

# fail on undefined variables
set -u

# Source setup-env.sh before tests
.  share/spack/setup-env.sh

# bash should expand aliases even when non-interactive
if [ -n "${BASH:-}" ]; then
    shopt -s expand_aliases
fi

title "Testing setup-env.sh with $_sp_shell"

# spack command is now avaialble
succeeds which spack

# mock cd command (intentionally define only AFTER setup-env.sh)
cd() {
    echo cd "$@"
}

# create a fake mock package install and store its location for later
title "Setup"
echo "Creating a mock package installation"
spack -m install --fake a
a_install=$(spack location -i a)
a_module=$(spack -m module tcl find a)
a_dotkit=$(spack -m module dotkit find a)

b_install=$(spack location -i b)
b_module=$(spack -m module tcl find b)
b_dotkit=$(spack -m module dotkit find b)

# create a test environment for tesitng environment commands
echo "Creating a mock environment"
spack env create spack_test_env
test_env_location=$(spack location -e spack_test_env)

# ensure that we uninstall b on exit
cleanup() {
    if [ "$?" != 0 ]; then
        trapped_error=true
    else
        trapped_error=false
    fi

    echo "Removing test environment before exiting."
    spack env deactivate 2>1 > /dev/null
    spack env rm -y spack_test_env

    title "Cleanup"
    echo "Removing test packages before exiting."
    spack -m uninstall -yf b a

    echo
    echo "$success tests succeeded."
    echo "$errors tests failed."

    if [ "$trapped_error" = true ]; then
        echo "Exited due to an error."
    fi

    if [ "$errors" = 0 ] && [ "$trapped_error" = false ]; then
        pass
        exit 0
    else
        fail
        exit 1
    fi
}
trap cleanup EXIT

# -----------------------------------------------------------------------
# Test all spack commands with special env support
# -----------------------------------------------------------------------
title 'Testing `spack`'
contains 'usage: spack ' spack
contains "usage: spack " spack -h
contains "usage: spack " spack help
contains "usage: spack " spack -H
contains "usage: spack " spack help --all

title 'Testing `spack cd`'
contains "usage: spack cd " spack cd -h
contains "usage: spack cd " spack cd --help
contains "cd $b_install" spack cd -i b

title 'Testing `spack module`'
contains "usage: spack module " spack -m module -h
contains "usage: spack module " spack -m module --help
contains "usage: spack module " spack -m module

title 'Testing `spack load`'
contains "module load $b_module" spack -m load b
fails spack -m load -l
contains "module load -l --arg $b_module" spack -m load -l --arg b
contains "module load $b_module $a_module" spack -m load -r a
contains "module load $b_module $a_module" spack -m load --dependencies a
fails spack -m load d
contains "usage: spack load " spack -m load -h
contains "usage: spack load " spack -m load -h d
contains "usage: spack load " spack -m load --help

title 'Testing `spack unload`'
contains "module unload $b_module" spack -m unload b
fails spack -m unload -l
contains "module unload -l --arg $b_module" spack -m unload -l --arg b
fails spack -m unload d
contains "usage: spack unload " spack -m unload -h
contains "usage: spack unload " spack -m unload -h d
contains "usage: spack unload " spack -m unload --help

title 'Testing `spack use`'
contains "use $b_dotkit" spack -m use b
fails spack -m use -l
contains "use -l --arg $b_dotkit" spack -m use -l --arg b
contains "use $b_dotkit $a_dotkit" spack -m use -r a
contains "use $b_dotkit $a_dotkit" spack -m use --dependencies a
fails spack -m use d
contains "usage: spack use " spack -m use -h
contains "usage: spack use " spack -m use -h d
contains "usage: spack use " spack -m use --help

title 'Testing `spack unuse`'
contains "unuse $b_dotkit" spack -m unuse b
fails spack -m unuse -l
contains "unuse -l --arg $b_dotkit" spack -m unuse -l --arg b
fails spack -m unuse d
contains "usage: spack unuse "  spack -m unuse -h
contains "usage: spack unuse "  spack -m unuse -h d
contains "usage: spack unuse "  spack -m unuse --help

title 'Testing `spack env`'
contains "usage: spack env " spack env -h
contains "usage: spack env " spack env --help

title 'Testing `spack env list`'
contains " spack env list " spack env list -h
contains " spack env list " spack env list --help

title 'Testing `spack env activate`'
contains "No such environment:" spack env activate no_such_environment
contains "usage: spack env activate " spack env activate
contains "usage: spack env activate " spack env activate -h
contains "usage: spack env activate " spack env activate --help

title 'Testing `spack env deactivate`'
contains "Error: No environment is currently active" spack env deactivate
contains "usage: spack env deactivate " spack env deactivate no_such_environment
contains "usage: spack env deactivate " spack env deactivate -h
contains "usage: spack env deactivate " spack env deactivate --help

title 'Testing activate and deactivate together'
echo "Testing 'spack env activate spack_test_env'"
spack env activate spack_test_env
is_set SPACK_ENV

echo "Testing 'spack env deactivate'"
spack env deactivate
is_not_set SPACK_ENV

echo "Testing 'spack env activate spack_test_env'"
spack env activate spack_test_env
is_set SPACK_ENV

echo "Testing 'despacktivate'"
despacktivate
is_not_set SPACK_ENV

echo "Testing 'spack env activate --prompt spack_test_env'"
spack env activate --prompt spack_test_env
is_set SPACK_ENV
is_set SPACK_OLD_PS1

echo "Testing 'despacktivate'"
despacktivate
is_not_set SPACK_ENV
is_not_set SPACK_OLD_PS1
