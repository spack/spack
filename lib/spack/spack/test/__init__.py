##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import sys
import unittest

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack

"""Names of tests to be included in Spack's test suite"""
test_names = ['versions',
              'url_parse',
              'url_substitution',
              'packages',
              'stage',
              'spec_syntax',
              'spec_semantics',
              'spec_dag',
              'concretize',
              'multimethod',
              'install',
              'package_sanity',
              'config',
              'directory_layout',
              'python_version',
              'git_fetch',
              'svn_fetch',
              'hg_fetch',
              'mirror',
              'url_extrapolate',
              'cc',
              'link_tree',
              'spec_yaml',
              'optional_deps',
              'make_executable',
              'configure_guess',
              'unit_install',
              'lock',
              'database']


def list_tests():
    """Return names of all tests that can be run for Spack."""
    return test_names


def run(names, verbose=False):
    """Run tests with the supplied names.  Names should be a list.  If
       it's empty, run ALL of Spack's tests."""
    verbosity = 1 if not verbose else 2

    if not names:
        names = test_names
    else:
        for test in names:
            if test not in test_names:
                tty.error("%s is not a valid spack test name." % test,
                          "Valid names are:")
                colify(sorted(test_names), indent=4)
                sys.exit(1)

    runner = unittest.TextTestRunner(verbosity=verbosity)

    testsRun = errors = failures = 0
    for test in names:
        module = 'spack.test.' + test
        print module
        suite = unittest.defaultTestLoader.loadTestsFromName(module)

        tty.msg("Running test: %s" % test)
        result = runner.run(suite)
        testsRun += result.testsRun
        errors   += len(result.errors)
        failures += len(result.failures)

    succeeded = not errors and not failures
    tty.msg("Tests Complete.",
            "%5d tests run" % testsRun,
            "%5d failures" % failures,
            "%5d errors" % errors)

    if not errors and not failures:
        tty.info("OK", format='g')
    else:
        tty.info("FAIL", format='r')
        sys.exit(1)
