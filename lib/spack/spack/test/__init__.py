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
import sys
import os

import llnl.util.tty as tty
import nose
import spack
import spack.architecture
from llnl.util.filesystem import join_path
from llnl.util.tty.colify import colify
from spack.test.tally_plugin import Tally
from spack.platforms.test import Test as TestPlatform
"""Names of tests to be included in Spack's test suite"""

# All the tests Spack knows about.
# Keep these one per line so that it's easy to see changes in diffs.
test_names = [
    'architecture',
    'build_system_guess',
    'cc',
    'cmd.find',
    'cmd.module',
    'cmd.install',
    'cmd.uninstall',
    'concretize',
    'concretize_preferences',
    'config',
    'database',
    'directory_layout',
    'environment',
    'file_cache',
    'git_fetch',
    'hg_fetch',
    'install',
    'library_list',
    'link_tree',
    'lock',
    'make_executable',
    'mirror',
    'modules',
    'multimethod',
    'namespace_trie',
    'optional_deps',
    'package_sanity',
    'packages',
    'pattern',
    'python_version',
    'sbang',
    'spec_dag',
    'spec_semantics',
    'spec_syntax',
    'spec_yaml',
    'stage',
    'svn_fetch',
    'url_extrapolate',
    'url_parse',
    'url_substitution',
    'versions',
    'provider_index',
    'spack_yaml',
    # This test needs to be last until global compiler cache is fixed.
    'cmd.test_compiler_cmd',
]


def setup_tests():
    """Prepare the environment for the Spack tests to be run."""
    test_platform = TestPlatform()
    spack.architecture.real_platform = spack.architecture.platform
    spack.architecture.platform = lambda: test_platform


def list_tests():
    """Return names of all tests that can be run for Spack."""
    return test_names


def run(names, outputDir, verbose=False):
    """Run tests with the supplied names.  Names should be a list.  If
       it's empty, run ALL of Spack's tests."""
    # Print output to stdout if verbose is 1.
    if verbose:
        os.environ['NOSE_NOCAPTURE'] = '1'

    if not names:
        names = test_names
    else:
        for test in names:
            if test not in test_names:
                tty.error("%s is not a valid spack test name." % test,
                          "Valid names are:")
                colify(sorted(test_names), indent=4)
                sys.exit(1)

    tally = Tally()

    modules = ['spack.test.' + test for test in names]
    runOpts = ["--with-%s" % spack.test.tally_plugin.Tally.name]

    if outputDir:
        xmlOutputFname = "unittests-{0}.xml".format(test)
        xmlOutputPath = join_path(outputDir, xmlOutputFname)
        runOpts += ["--with-xunit",
                    "--xunit-file={0}".format(xmlOutputPath)]
    argv = [""] + runOpts + modules

    setup_tests()
    nose.run(argv=argv, addplugins=[tally])

    succeeded = not tally.failCount and not tally.errorCount
    tty.msg(
        "Tests Complete.",
        "%5d tests run" % tally.numberOfTestsRun,
        "%5d failures" % tally.failCount,
        "%5d errors" % tally.errorCount
    )

    if tally.fail_list:
        items = [x for x in tally.fail_list]
        tty.msg('List of failing tests:', *items)

    if tally.error_list:
        items = [x for x in tally.error_list]
        tty.msg('List of tests with errors:', *items)

    if succeeded:
        tty.info("OK", format='g')
    else:
        tty.info("FAIL", format='r')
        sys.exit(1)
