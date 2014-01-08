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

import spack.packages as packages
from spack.spec import Spec
from spack.test.mock_packages_test import *

class ConcretizeTest(MockPackagesTest):

    def check_spec(self, abstract, concrete):
        if abstract.versions.concrete:
            self.assertEqual(abstract.versions, concrete.versions)

        if abstract.variants:
            self.assertEqual(abstract.versions, concrete.versions)

        if abstract.compiler and abstract.compiler.concrete:
            self.assertEqual(abstract.compiler, concrete.compiler)

        if abstract.architecture and abstract.architecture.concrete:
            self.assertEqual(abstract.architecture, concrete.architecture)


    def check_concretize(self, abstract_spec):
        abstract = Spec(abstract_spec)
        concrete = abstract.concretized()

        self.assertFalse(abstract.concrete)
        self.assertTrue(concrete.concrete)
        self.check_spec(abstract, concrete)

        return concrete


    def test_concretize_no_deps(self):
        self.check_concretize('libelf')
        self.check_concretize('libelf@0.8.13')


    def test_concretize_dag(self):
        self.check_concretize('callpath')
        self.check_concretize('mpileaks')
        self.check_concretize('libelf')


    def test_concretize_with_virtual(self):
        self.check_concretize('mpileaks ^mpi')
        self.check_concretize('mpileaks ^mpi@:1.1')
        self.check_concretize('mpileaks ^mpi@2:')
        self.check_concretize('mpileaks ^mpi@2.1')
        self.check_concretize('mpileaks ^mpi@2.2')
        self.check_concretize('mpileaks ^mpi@2.2')
        self.check_concretize('mpileaks ^mpi@:1')
        self.check_concretize('mpileaks ^mpi@1.2:2')


    def test_concretize_with_restricted_virtual(self):
        self.check_concretize('mpileaks ^mpich2')

        concrete = self.check_concretize('mpileaks   ^mpich2@1.1')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.1'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.2')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.2'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.5')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.5'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.3')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.3'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.2')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.2'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.1')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.1'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.1:')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.1:'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.5:')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.5:'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.3.1:1.4')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.3.1:1.4'))


    def test_concretize_with_provides_when(self):
        """Make sure insufficient versions of MPI are not in providers list when
           we ask for some advanced version.
        """
        self.assertTrue(not any(spec.satisfies('mpich2@:1.0')
                                for spec in packages.providers_for('mpi@2.1')))

        self.assertTrue(not any(spec.satisfies('mpich2@:1.1')
                                for spec in packages.providers_for('mpi@2.2')))

        self.assertTrue(not any(spec.satisfies('mpich2@:1.1')
                                for spec in packages.providers_for('mpi@2.2')))

        self.assertTrue(not any(spec.satisfies('mpich@:1')
                                for spec in packages.providers_for('mpi@2')))

        self.assertTrue(not any(spec.satisfies('mpich@:1')
                                for spec in packages.providers_for('mpi@3')))

        self.assertTrue(not any(spec.satisfies('mpich2')
                                for spec in packages.providers_for('mpi@3')))


    def test_virtual_is_fully_expanded_for_callpath(self):
        # force dependence on fake "zmpi" by asking for MPI 10.0
        spec = Spec('callpath ^mpi@10.0')
        self.assertIn('mpi', spec.dependencies)
        self.assertNotIn('fake', spec)

        spec.concretize()

        self.assertIn('zmpi', spec.dependencies)
        self.assertNotIn('mpi', spec)
        self.assertIn('fake', spec.dependencies['zmpi'])


    def test_virtual_is_fully_expanded_for_mpileaks(self):
        spec = Spec('mpileaks ^mpi@10.0')
        self.assertIn('mpi', spec.dependencies)
        self.assertNotIn('fake', spec)

        spec.concretize()

        self.assertIn('zmpi', spec.dependencies)
        self.assertIn('callpath', spec.dependencies)
        self.assertIn('zmpi', spec.dependencies['callpath'].dependencies)
        self.assertIn('fake', spec.dependencies['callpath'].dependencies['zmpi'].dependencies)

        self.assertNotIn('mpi', spec)


    def test_my_dep_depends_on_provider_of_my_virtual_dep(self):
        spec = Spec('indirect_mpich')
        spec.normalize()

        print
        print spec.tree(color=True)

        spec.concretize()
