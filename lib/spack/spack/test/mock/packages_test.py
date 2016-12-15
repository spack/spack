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
import collections

import spack
import spack.config
from llnl.util.filesystem import mkdirp, join_path
from ordereddict_backport import OrderedDict
from spack.repository import RepoPath

platform = spack.architecture.platform()

linux_os_name = 'debian'
linux_os_version = '6'

if platform.name == 'linux':
    linux_os = platform.operating_system("default_os")
    linux_os_name = linux_os.name
    linux_os_version = linux_os.version

cmp_yaml = join_path(spack.test_path, 'data', 'compilers.yaml')
LinuxOS = collections.namedtuple('LinuxOS', ['name', 'version'])
with open(cmp_yaml) as f:
    mock_compiler_config = ''.join(f.readlines()).format(
        LinuxOS(name=linux_os_name, version=linux_os_version)
    )

pkg_yaml = join_path(spack.test_path, 'data', 'packages.yaml')
with open(pkg_yaml) as f:
    mock_packages_config = ''.join(f.readlines())

cfg_yaml = join_path(spack.test_path, 'data', 'config.yaml')
with open(cfg_yaml) as f:
    mock_config = ''.join(f.readlines())

# these are written out to mock config files.
mock_configs = {
    'config.yaml': mock_config,
    'compilers.yaml': mock_compiler_config,
    'packages.yaml': mock_packages_config,
}


class MockPackagesTest(unittest.TestCase):

    def setUp(self):
        # Use the mock packages database for these tests.  This allows
        # us to set up contrived packages that don't interfere with
        # real ones.
        self.db = RepoPath(spack.mock_packages_path)
        spack.repo.swap(self.db)

        # Mock up temporary configuration directories
        self.temp_config = tempfile.mkdtemp()
        self.mock_site_config = os.path.join(self.temp_config, 'site')
        self.mock_user_config = os.path.join(self.temp_config, 'user')
        mkdirp(self.mock_site_config)
        mkdirp(self.mock_user_config)
        for filename, data in mock_configs.items():
            conf_yaml = os.path.join(self.mock_site_config, filename)
            with open(conf_yaml, 'w') as f:
                f.write(data)

        # TODO: Mocking this up is kind of brittle b/c ConfigScope
        # TODO: constructor modifies config_scopes.  Make it cleaner.
        spack.config.clear_config_caches()
        self.real_scopes = spack.config.config_scopes

        spack.config.config_scopes = OrderedDict()
        spack.config.ConfigScope('site', self.mock_site_config)
        spack.config.ConfigScope('user', self.mock_user_config)

        # Keep tests from interfering with the actual module path.
        self.real_share_path = spack.share_path
        spack.share_path = tempfile.mkdtemp()

        # Store changes to the package's dependencies so we can
        # restore later.
        self.saved_deps = {}

    def set_pkg_dep(self, pkg_name, spec, deptypes=spack.alldeps):
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
        # XXX(deptype): handle deptypes.
        pkg.dependencies[spec.name] = {Spec(pkg_name): spec}
        pkg.dependency_types[spec.name] = set(deptypes)

    def tearDown(self):
        """Restore the real packages path after any test."""
        spack.repo.swap(self.db)
        spack.config.config_scopes = self.real_scopes

        shutil.rmtree(self.temp_config, ignore_errors=True)
        spack.config.clear_config_caches()

        # XXX(deptype): handle deptypes.
        # Restore dependency changes that happened during the test
        for pkg_name, (pkg, deps) in self.saved_deps.items():
            pkg.dependencies.clear()
            pkg.dependencies.update(deps)

        shutil.rmtree(spack.share_path, ignore_errors=True)
        spack.share_path = self.real_share_path
