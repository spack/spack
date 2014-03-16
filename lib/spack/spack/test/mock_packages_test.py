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
from spack.packages import PackageDB
from spack.spec import Spec

mock_packages_path = join_path(spack.module_path, 'test', 'mock_packages')

def set_pkg_dep(pkg, spec):
    """Alters dependence information for a pacakge.
       Use this to mock up constraints.
    """
    spec = Spec(spec)
    spack.db.get(pkg).dependencies[spec.name] = spec


class MockPackagesTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        # Use the mock packages database for these tests.  This allows
        # us to set up contrived packages that don't interfere with
        # real ones.
        self.real_db = spack.db
        spack.db = PackageDB(mock_packages_path)


    @classmethod
    def tearDown(self):
        """Restore the real packages path after any test."""
        #restore_dependencies()
        spack.db = self.real_db
