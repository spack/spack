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
import unittest

from llnl.util.lang import list_modules
from llnl.util.filesystem import join_path

import spack
import spack.packages as packages
from spack.spec import Spec

mock_packages_path = join_path(spack.module_path, 'test', 'mock_packages')
original_deps = None


def set_pkg_dep(pkg, spec):
    """Alters dependence information for a pacakge.
       Use this to mock up constraints.
    """
    spec = Spec(spec)
    packages.get(pkg).dependencies[spec.name] = spec


def restore_dependencies():
    # each time through restore original dependencies & constraints
    global original_deps
    for pkg_name, deps in original_deps.iteritems():
        packages.get(pkg_name).dependencies.clear()
        for dep in deps:
            set_pkg_dep(pkg_name, dep)


class MockPackagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a different packages directory for these tests.  We want to use
        # mocked up packages that don't interfere with the real ones.
        cls.real_packages_path = spack.packages_path
        spack.packages_path = mock_packages_path

        # First time through, record original relationships bt/w packages
        global original_deps
        original_deps = {}
        for name in list_modules(mock_packages_path):
            pkg = packages.get(name)
            original_deps[name] = [
                spec for spec in pkg.dependencies.values()]


    @classmethod
    def tearDownClass(cls):
        """Restore the real packages path after any test."""
        restore_dependencies()
        spack.packages_path = cls.real_packages_path


    def setUp(self):
        """Before each test, restore deps between packages to original state."""
        restore_dependencies()
