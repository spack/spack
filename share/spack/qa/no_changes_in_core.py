#!/usr/bin/env spack-python
#
# Description:
#     Helper script that returns 0 if any file in core
#     has been changed, 1 otherwise
#
# Usage:
#     nochanges_in_core.py && [command run if there are no changes in core]
#

import sys
import os.path

import spack.spec
import spack.cmd.flake8

# Get the complete list of files that changed
files = spack.cmd.flake8.changed_files(True)

# If something changed in the core libraries we need to test it
core_path = os.path.join('lib', 'spack')
changes_in_core = any(core_path in x for x in files)

# Exit early because polling the repo may be slow
if changes_in_core:
    print('FAILURE: at least one core file has been modified.')
    print('Rename your branch to something that does not start with "packages"')  # noqa: ignore=E501
    sys.exit(1)

# If we changed any of the packages that are under build tests
# we consider it a change in core

build_tests = (
    'mpich',
    'astyle',
    'tut',
    'py-setuptools',
    'openjpeg',
    'r-rcpp'
)

specs = [spack.spec.Spec(x) for x in build_tests]
for s in specs:
    s.concretize()

names = []
for s in specs:
    names.extend([d.name for d in s.traverse()])

names = [os.path.join(x, 'package.py') for x in names]
names = sorted(set(names))

changes_in_relevant_packages = any(name in x for x in files for name in names)

if changes_in_relevant_packages:
    print('FAILURE: at least one of the packages in the "Build tests" stage has been modified.')  # noqa: ignore=E501
    print('Rename your branch to something that does not start with "packages"')  # noqa: ignore=E501
    sys.exit(1)

sys.exit(0)
