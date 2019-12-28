#!/usr/bin/env fish
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

#################################################################################
# This file is part of Spack's fish (friendly interactive shell) support
# Ported from bash (setup-env-test.sh) by Johannes Blaschke,
#                                      johannes@blaschke.science
#################################################################################


function allocate_testing_global -d "allocate global variables used for testing"

    # Colors for output
    set -gx __spt_red '\033[1;31m'
    set -gx __spt_cyan '\033[1;36m'
    set -gx __spt_green '\033[1;32m'
    set -gx __spt_reset '\033[0m'

    # counts of test successes and failures.
    set -gx __spt_success 0
    set -gx __spt_errors 0
end


function delete_testing_global -d "deallocate global varialbes used for testing"

    set -e __spt_red
    set -e __spt_cyan
    set -e __spt_green
    set -e __spt_reset

    set -e __spt_success
    set -e __spt_errors
end

# ------------------------------------------------------------------------
# Functions for color output.
# ------------------------------------------------------------------------


function echo_red
    printf "$__spt_red$argv$__spt_reset\n"
end

function echo_green
    printf "$__spt_green$argv$__spt_reset\n"
end

function echo_msg
    printf "$__spt_cyan$argv$__spt_reset\n"
end



# ------------------------------------------------------------------------
# Generic functions for testing fish code.
# ------------------------------------------------------------------------


# Print out a header for a group of tests.
function title

    echo
    echo_msg "$argv"
    echo_msg "---------------------------------"

end

# echo FAIL in red text; increment failures
function fail
    echo_red FAIL
    set __spt_errors (math $__spt_errors+1)
end

# echo SUCCESS in green; increment successes
function pass
    echo_green SUCCESS
    set __spt_success (math $__spt_success+1)
end


#
# Run a command and suppress output unless it fails.
# On failure, echo the exit code and output.
#
function spt_succeeds
    printf "'$argv' succeeds ... "

    set -l output (eval $argv 2>&1)

    if test $status -ne 0
        fail
        echo_red "Command failed with error $status"
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Run a command and suppress output unless it succeeds.
# If the command succeeds, echo the output.
#
function spt_fails
    printf "'$argv' fails ... "

    set -l output (eval $argv 2>&1)

    if test $status -eq 0
        fail
        echo_red "Command failed with error $status"
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Ensure that a string is in the output of a command.
# Suppresses output on success.
# On failure, echo the exit code and output.
#
function spt_contains
    set -l target_string $argv[1]
    set -l remaining_args $argv[2..-1]

    printf "'$remaining_args' output contains '$target_string'"

    set -l output (eval $remaining_args 2>&1)

    if not echo "$output" | string match -q -r ".*$target_string.*"
        fail
        echo_red "Command exited with error $status"
        echo_red "'$target_string' was not in output."
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Ensure that a variable is set.
#
function is_set
    prinf "'$argv[1]' is set ... "

    if test -z "$argv[1]"
        fail
        echo_msg "'$argv[1]' was not set!"
    else
        pass
    end
end


#
# Ensure that a variable is not set.
# Fails and prints the value of the variable if it is set.
#
function is_not_set
    prinf "'$argv[1]' is not set ... "

    if test -n "$argv[1]"
        fail
        echo_msg "'$argv[1]' was set!"
        echo "    $argv[1]"
    else
        pass
    end
end



# -----------------------------------------------------------------------
# Instead of invoking the module commands, we print the
# arguments that Spack invokes the command with, so we can check that
# Spack passes the expected arguments in the tests below.
#
# We make that happen by defining the sh functions below.
# -----------------------------------------------------------------------

function spt_module
    echo "module $argv"
end

# mock cd command (intentionally define only AFTER setup-env.sh)
function spt_cd
    echo "cd $argv"
end



# -----------------------------------------------------------------------
# Setup test environment and do some preliminary checks
# -----------------------------------------------------------------------

# Make sure no environment is active
set -e SPACK_ENV
true # ingnore failing `set -e`

# Source setup-env.sh before tests
source share/spack/setup-env.fish

allocate_testing_global


title "Testing setup-env.fish with $_sp_shell"

# spack command is now avaialble
spt_succeeds which spack


# create a fake mock package install and store its location for later
title "Setup"
echo "Creating a mock package installation"
spack -m install --fake a
set a_install (spack location -i a)
set a_module (spack -m module tcl find a)

set b_install (spack location -i b)
set b_module (spack -m module tcl find b)

# create a test environment for tesitng environment commands
echo "Creating a mock environment"
spack env create spack_test_env
set test_env_location (spack location -e spack_test_env)

# ensure that we uninstall b on exit
function spt_cleanup

    set trapped_error false
    if test $status -ne 0
        set trapped_error true
    end

    echo "Removing test environment before exiting."
    spack env deactivate 2>&1 > /dev/null
    spack env rm -y spack_test_env

    title "Cleanup"
    echo "Removing test packages before exiting."
    spack -m uninstall -yf b a

    echo
    echo "$__spt_success tests succeeded."
    echo "$__spt_errors tests failed."

    if test "$trapped_error" = false
        echo "Exited due to an error."
    end

    if test "$__spt_errors" -eq 0
        if test "$trapped_error" = false
            pass
            exit 0
        else
            fail
            exit 1
        end
    else
        fail
        exit 1
    end

    delete_testing_global
end

trap spt_cleanup EXIT



# -----------------------------------------------------------------------
# Test all spack commands with special env support
# -----------------------------------------------------------------------
title 'Testing `spack`'
spt_contains 'usage: spack ' spack
spt_contains "usage: spack " spack -h
spt_contains "usage: spack " spack help
spt_contains "usage: spack " spack -H
spt_contains "usage: spack " spack help --all

