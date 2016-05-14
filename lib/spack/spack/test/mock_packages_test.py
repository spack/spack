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
import os
import shutil
import tempfile
import unittest

import spack
import spack.config
from llnl.util.filesystem import mkdirp
from ordereddict_backport import OrderedDict
from spack.repository import RepoPath
from spack.spec import Spec

mock_compiler_config = """\
compilers:
  all:
    clang@3.3:
      cc: /path/to/clang
      cxx: /path/to/clang++
      f77: None
      fc: None
    gcc@4.5.0:
      cc: /path/to/gcc
      cxx: /path/to/g++
      f77: /path/to/gfortran
      fc: /path/to/gfortran
"""

mock_packages_config = """\
packages:
  externaltool:
    buildable: False
    paths:
      externaltool@1.0%gcc@4.5.0: /path/to/external_tool
  externalvirtual:
    buildable: False
    paths:
      externalvirtual@2.0%clang@3.3: /path/to/external_virtual_clang
      externalvirtual@1.0%gcc@4.5.0: /path/to/external_virtual_gcc
"""

class MockPackagesTest(unittest.TestCase):
    def initmock(self):
        # Use the mock packages database for these tests.  This allows
        # us to set up contrived packages that don't interfere with
        # real ones.
        self.db = RepoPath(spack.mock_packages_path)
        spack.repo.swap(self.db)

        spack.config.clear_config_caches()
        self.real_scopes = spack.config.config_scopes

        # Mock up temporary configuration directories
        self.temp_config = tempfile.mkdtemp()
        self.mock_site_config = os.path.join(self.temp_config, 'site')
        self.mock_user_config = os.path.join(self.temp_config, 'user')
        mkdirp(self.mock_site_config)
        mkdirp(self.mock_user_config)
        for confs in [('compilers.yaml', mock_compiler_config), ('packages.yaml', mock_packages_config)]:
            conf_yaml = os.path.join(self.mock_site_config, confs[0])
            with open(conf_yaml, 'w') as f:
                f.write(confs[1])

        # TODO: Mocking this up is kind of brittle b/c ConfigScope
        # TODO: constructor modifies config_scopes.  Make it cleaner.
        spack.config.config_scopes = OrderedDict()
        spack.config.ConfigScope('site', self.mock_site_config)
        spack.config.ConfigScope('user', self.mock_user_config)

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
        shutil.rmtree(self.temp_config, ignore_errors=True)
        spack.config.clear_config_caches()

        # Restore dependency changes that happened during the test
        for pkg_name, (pkg, deps) in self.saved_deps.items():
            pkg.dependencies.clear()
            pkg.dependencies.update(deps)


    def setUp(self):
        self.initmock()


    def tearDown(self):
        self.cleanmock()
