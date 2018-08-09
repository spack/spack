#!/bin/bash -e
#
# Description:
#     Common setup code to be sourced by Spack's test scripts.
#

QA_DIR="$(dirname ${BASH_SOURCE[0]})"
SPACK_ROOT="$QA_DIR/../../.."

# Source the setup script
. "$SPACK_ROOT/share/spack/setup-env.sh"

# Set up some variables for running coverage tests.
if [[ "$TEST_SUITE" == "unit" || "$TEST_SUITE" == "build" ]]; then
    coverage=coverage
    coverage_run="coverage run"
else
    coverage=""
    coverage_run=""
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

        # Flake8 and Sphinx require setuptools in order to run.
        # Otherwise, they print out this error message:
        #
        #   Traceback (most recent call last):
        #     File: "/usr/bin/flake8", line 5, in <module>
        #       from pkg_resources import load_entry_point
        #   ImportError: No module named pkg_resources
        #
        # Print a more useful error message if setuptools not found.
        if [[ $dep == flake8 || $dep == sphinx* ]]; then
            # Find which Python is being run
            # Spack-installed packages have a hard-coded shebang
            python_cmd=$(head -n 1 $(which $dep) | cut -c 3-)
            # May not have a shebang
            if [[ $python_cmd != *python* ]]; then
                python_cmd=python
            fi
            # Check if setuptools is in the PYTHONPATH
            if ! $python_cmd -c "import setuptools" 2> /dev/null; then
                echo "ERROR: setuptools is required to run $dep."
                echo "Please add it to your PYTHONPATH."

                exit 1
            fi
        fi
    done
    echo "Dependencies found."
}
