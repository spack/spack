#!/bin/bash -e
#
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Description:
#     Common setup code to be sourced by Spack's test scripts.
#

QA_DIR="$(dirname ${BASH_SOURCE[0]})"
export SPACK_ROOT=$(realpath "$QA_DIR/../../..")

# Source the setup script
. "$SPACK_ROOT/share/spack/setup-env.sh"

# Ensure that clingo is bootstrapped
spack spec zlib > /dev/null

# by default coverage is off.
coverage=""
coverage_run=""

# Set up some variables for running coverage tests.
if [[ "$COVERAGE" == "true" ]]; then
    # these set up coverage for Python
    coverage=coverage
    coverage_run="coverage run"

    # bash coverage depends on some other factors
    mkdir -p coverage
    bashcov=$(realpath ${QA_DIR}/bashcov)

    # instrument scripts requiring shell coverage
    if [ "$(uname -o)" != "Darwin" ]; then
        # On darwin, #! interpreters must be binaries, so no sbang for bashcov
        sed -i "s@#\!/bin/sh@#\!${bashcov}@"   "$SPACK_ROOT/bin/sbang"
    fi
fi

#
# Description:
#     Check to see if dependencies are installed.
#     If not, warn the user and tell them how to
#     install these dependencies.
#
# Usage:
#     check-deps <dep> ...
#
# Options:
#     One or more dependencies. Must use name of binary.
check_dependencies() {
    for dep in "$@"; do
        if ! which $dep &> /dev/null; then
            # Map binary name to package name
            case $dep in
                sphinx-apidoc|sphinx-build)
                    spack_package=py-sphinx
                    pip_package=sphinx
                    ;;
                coverage)
                    spack_package=py-coverage
                    pip_package=coverage
                    ;;
                flake8)
                    spack_package=py-flake8
                    pip_package=flake8
                    ;;
                mypy)
                    spack_package=py-mypy
                    pip_package=mypy
                    ;;
                dot)
                    spack_package=graphviz
                    ;;
                git)
                    spack_package=git
                    ;;
                hg)
                    spack_package=mercurial
                    pip_package=mercurial
                    ;;
                kcov)
                    spack_package=kcov
                    ;;
                svn)
                    spack_package=subversion
                    ;;
                *)
                    spack_package=$dep
                    pip_package=$dep
                    ;;
            esac

            echo "ERROR: $dep is required to run this script."
            echo

            if [[ $spack_package ]]; then
                echo "To install with Spack, run:"
                echo "    $ spack install $spack_package"
            fi

            if [[ $pip_package ]]; then
                echo "To install with pip, run:"
                echo "    $ pip install $pip_package"
            fi

            if [[ $spack_package || $pip_package ]]; then
                echo "Then add the bin directory to your PATH."
            fi

            exit 1
        fi
    done
    echo "Dependencies found."
}
