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
import spack
import spack.architecture
from spack.test.mock_packages_test import *
from tempfile import mkdtemp


class ConcretizePreferencesTest(MockPackagesTest):
    """Test concretization preferences are being applied correctly.
    """

    def setUp(self):
        """Create config section to store concretization preferences
        """
        super(ConcretizePreferencesTest, self).setUp()
        self.tmp_dir = mkdtemp('.tmp', 'spack-config-test-')
        spack.config.ConfigScope('concretize',
                                 os.path.join(self.tmp_dir, 'concretize'))

    def tearDown(self):
        super(ConcretizePreferencesTest, self).tearDown()
        shutil.rmtree(self.tmp_dir, True)
        spack.pkgsort = spack.PreferredPackages()

    def concretize(self, abstract_spec):
        return Spec(abstract_spec).concretized()

    def update_packages(self, pkgname, section, value):
        """Update config and reread package list"""
        conf = {pkgname: {section: value}}
        spack.config.update_config('packages', conf, 'concretize')
        spack.pkgsort = spack.PreferredPackages()

    def assert_variant_values(self, spec, **variants):
        concrete = self.concretize(spec)
        for variant, value in variants.items():
            self.assertEqual(concrete.variants[variant].value, value)

    def test_preferred_variants(self):
        """Test preferred variants are applied correctly
        """
        self.update_packages('mpileaks', 'variants',
                             '~debug~opt+shared+static')
        self.assert_variant_values('mpileaks', debug=False, opt=False,
                                   shared=True, static=True)

        self.update_packages('mpileaks', 'variants',
                             ['+debug', '+opt', '~shared', '-static'])
        self.assert_variant_values('mpileaks', debug=True, opt=True,
                                   shared=False, static=False)

    def test_preferred_compilers(self):
        """Test preferred compilers are applied correctly
        """
        self.update_packages('mpileaks', 'compiler', ['clang@3.3'])
        spec = self.concretize('mpileaks')
        self.assertEqual(spec.compiler, spack.spec.CompilerSpec('clang@3.3'))

        self.update_packages('mpileaks', 'compiler', ['gcc@4.5.0'])
        spec = self.concretize('mpileaks')
        self.assertEqual(spec.compiler, spack.spec.CompilerSpec('gcc@4.5.0'))

    def test_preferred_versions(self):
        """Test preferred package versions are applied correctly
        """
        self.update_packages('mpileaks', 'version', ['2.3'])
        spec = self.concretize('mpileaks')
        self.assertEqual(spec.version, spack.spec.Version('2.3'))

        self.update_packages('mpileaks', 'version', ['2.2'])
        spec = self.concretize('mpileaks')
        self.assertEqual(spec.version, spack.spec.Version('2.2'))

    def test_preferred_providers(self):
        """Test preferred providers of virtual packages are applied correctly
        """
        self.update_packages('all', 'providers', {'mpi': ['mpich']})
        spec = self.concretize('mpileaks')
        self.assertTrue('mpich' in spec)

        self.update_packages('all', 'providers', {'mpi': ['zmpi']})
        spec = self.concretize('mpileaks')
        self.assertTrue('zmpi', spec)

    def test_develop(self):
        """Test conretization with develop version
        """
        spec = Spec('builtin.mock.develop-test')
        spec.concretize()
        self.assertEqual(spec.version, spack.spec.Version('0.2.15'))
