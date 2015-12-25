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

import spack
import spack.config
from spack.repository import RepoPath
from spack.spec import Spec


class MockPackagesTest(unittest.TestCase):
    def initmock(self):
        # Use the mock packages database for these tests.  This allows
        # us to set up contrived packages that don't interfere with
        # real ones.
        self.db = RepoPath(spack.mock_packages_path)
        spack.repo.swap(self.db)

        spack.config.clear_config_caches()
        self.real_scopes = spack.config.config_scopes
        self.real_valid_scopes = spack.config.valid_scopes
        spack.config.config_scopes = [
            spack.config.ConfigScope('site', spack.mock_site_config),
            spack.config.ConfigScope('user', spack.mock_user_config)]

        # Store changes to the package's dependencies so we can
        # restore later.
        self.saved_deps = {}


    def set_pkg_dep(self, pkg_name, spec):
        """Alters dependence information for a package.

        Adds a dependency on <spec> to pkg.
        Use this to mock up constraints.
        """
        spec = Spec(spec)

        # Save original dependencies before making any changes.
        pkg = spack.repo.get(pkg_name)
        if pkg_name not in self.saved_deps:
            self.saved_deps[pkg_name] = (pkg, pkg.dependencies.copy())

        # Change dep spec
        pkg.dependencies[spec.name] = { Spec(pkg_name) : spec }


    def cleanmock(self):
        """Restore the real packages path after any test."""
        spack.repo.swap(self.db)
        spack.config.config_scopes = self.real_scopes
        spack.config.valid_scopes = self.real_valid_scopes
        spack.config.clear_config_caches()

        # Restore dependency changes that happened during the test
        for pkg_name, (pkg, deps) in self.saved_deps.items():
            pkg.dependencies.clear()
            pkg.dependencies.update(deps)


    def setUp(self):
        self.initmock()


    def tearDown(self):
        self.cleanmock()
