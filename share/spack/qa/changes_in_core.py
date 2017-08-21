#!/usr/bin/env spack-python
#
# Description:
#     Helper script that returns 0 if any file in core
#     has been changed, 1 otherwise
#
# Usage:
#     changes_in_core.py && [command to be run if there are changes in core]
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
    sys.exit(0)

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
    sys.exit(0)

sys.exit(1)
