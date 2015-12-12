##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

import spack
import spack.config
from spack.packages import PackageDB
from spack.spec import Spec


def set_pkg_dep(pkg, spec):
    """Alters dependence information for a package.
       Use this to mock up constraints.
    """
    spec = Spec(spec)
    spack.db.get(pkg).dependencies[spec.name] = { Spec(pkg) : spec }


class MockPackagesTest(unittest.TestCase):
    def initmock(self):
        # Use the mock packages database for these tests.  This allows
        # us to set up contrived packages that don't interfere with
        # real ones.
        self.real_db = spack.db
        spack.db = PackageDB(spack.mock_packages_path)

        spack.config.clear_config_caches()
        self.real_scopes = spack.config.config_scopes
        spack.config.config_scopes = [
            ('site', spack.mock_site_config),
            ('user', spack.mock_user_config)]


    def cleanmock(self):
        """Restore the real packages path after any test."""
        spack.db = self.real_db
        spack.config.config_scopes = self.real_scopes
        spack.config.clear_config_caches()


    def setUp(self):
        self.initmock()


    def tearDown(self):
        self.cleanmock()


