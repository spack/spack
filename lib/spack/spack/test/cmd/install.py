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
import argparse
import codecs
import collections
import contextlib
import unittest
from six import StringIO

import llnl.util.filesystem
import spack
import spack.cmd
import spack.cmd.install as install

FILE_REGISTRY = collections.defaultdict(StringIO)


# Monkey-patch open to write module files to a StringIO instance
@contextlib.contextmanager
def mock_open(filename, mode, *args):
    if not mode == 'wb':
        message = 'test.test_install : unexpected opening mode for mock_open'
        raise RuntimeError(message)

    FILE_REGISTRY[filename] = StringIO()

    try:
        yield FILE_REGISTRY[filename]
    finally:
        handle = FILE_REGISTRY[filename]
        FILE_REGISTRY[filename] = handle.getvalue()
        handle.close()


class MockSpec(object):

    def __init__(self, name, version, hashStr=None):
        self._dependencies = {}
        self.name = name
        self.version = version
        self.hash = hashStr if hashStr else hash((name, version))

    def _deptype_norm(self, deptype):
        if deptype is None:
            return spack.alldeps
        # Force deptype to be a tuple so that we can do set intersections.
        if isinstance(deptype, str):
            return (deptype,)
        return deptype

    def _find_deps(self, where, deptype):
        deptype = self._deptype_norm(deptype)

        return [dep.spec
                for dep in where.values()
                if deptype and any(d in deptype for d in dep.deptypes)]

    def dependencies(self, deptype=None):
        return self._find_deps(self._dependencies, deptype)

    def dependents(self, deptype=None):
        return self._find_deps(self._dependents, deptype)

    def traverse(self, order=None):
        for _, spec in self._dependencies.items():
            yield spec.spec
        yield self

    def dag_hash(self):
        return self.hash

    @property
    def short_spec(self):
        return '-'.join([self.name, str(self.version), str(self.hash)])


class MockPackage(object):

    def __init__(self, spec, buildLogPath):
        self.name = spec.name
        self.spec = spec
        self.installed = False
        self.build_log_path = buildLogPath

    def do_install(self, *args, **kwargs):
        for x in self.spec.dependencies():
            x.package.do_install(*args, **kwargs)
        self.installed = True


class MockPackageDb(object):

    def __init__(self, init=None):
        self.specToPkg = {}
        if init:
            self.specToPkg.update(init)

    def get(self, spec):
        return self.specToPkg[spec]


def mock_fetch_log(path):
    return []


specX = MockSpec('X', '1.2.0')
specY = MockSpec('Y', '2.3.8')
specX._dependencies['Y'] = spack.spec.DependencySpec(
    specX, specY, spack.alldeps)
pkgX = MockPackage(specX, 'logX')
pkgY = MockPackage(specY, 'logY')
specX.package = pkgX
specY.package = pkgY


# TODO: add test(s) where Y fails to install
class InstallTestJunitLog(unittest.TestCase):
    """Tests test-install where X->Y"""

    def setUp(self):
        super(InstallTestJunitLog, self).setUp()
        install.PackageBase = MockPackage
        # Monkey patch parse specs

        def monkey_parse_specs(x, concretize):
            if x == ['X']:
                return [specX]
            elif x == ['Y']:
                return [specY]
            return []

        self.parse_specs = spack.cmd.parse_specs
        spack.cmd.parse_specs = monkey_parse_specs

        # Monkey patch os.mkdirp
        self.mkdirp = llnl.util.filesystem.mkdirp
        llnl.util.filesystem.mkdirp = lambda x: True

        # Monkey patch open
        self.codecs_open = codecs.open
        codecs.open = mock_open

        # Clean FILE_REGISTRY
        FILE_REGISTRY.clear()

        pkgX.installed = False
        pkgY.installed = False

        # Monkey patch pkgDb
        self.saved_db = spack.repo
        pkgDb = MockPackageDb({specX: pkgX, specY: pkgY})
        spack.repo = pkgDb

    def tearDown(self):
        # Remove the monkey patched test_install.open
        codecs.open = self.codecs_open

        # Remove the monkey patched os.mkdir
        llnl.util.filesystem.mkdirp = self.mkdirp
        del self.mkdirp

        # Remove the monkey patched parse_specs
        spack.cmd.parse_specs = self.parse_specs
        del self.parse_specs
        super(InstallTestJunitLog, self).tearDown()

        spack.repo = self.saved_db

    def test_installing_both(self):
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        args = parser.parse_args(['--log-format=junit', 'X'])
        install.install(parser, args)
        self.assertEqual(len(FILE_REGISTRY), 1)
        for _, content in FILE_REGISTRY.items():
            self.assertTrue('tests="2"' in content)
            self.assertTrue('failures="0"' in content)
            self.assertTrue('errors="0"' in content)

    def test_dependency_already_installed(self):
        pkgX.installed = True
        pkgY.installed = True
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        args = parser.parse_args(['--log-format=junit', 'X'])
        install.install(parser, args)
        self.assertEqual(len(FILE_REGISTRY), 1)
        for _, content in FILE_REGISTRY.items():
            self.assertTrue('tests="2"' in content)
            self.assertTrue('failures="0"' in content)
            self.assertTrue('errors="0"' in content)
            self.assertEqual(
                sum('skipped' in line for line in content.split('\n')), 2)
