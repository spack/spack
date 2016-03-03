##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
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
from spack.spec import Spec, CompilerSpec
from spack.test.mock_packages_test import *

class ConcretizeTest(MockPackagesTest):

    def check_normalize(self, spec_string, expected):
        spec = Spec(spec_string)
        spec.normalize()
        self.assertEqual(spec, expected)
        self.assertTrue(spec.eq_dag(expected))


    def test_normalize_simple_conditionals(self):
        self.check_normalize('optional-dep-test', Spec('optional-dep-test'))
        self.check_normalize('optional-dep-test~a', Spec('optional-dep-test~a'))

        self.check_normalize('optional-dep-test+a',
                             Spec('optional-dep-test+a', Spec('a')))

        self.check_normalize('optional-dep-test@1.1',
                             Spec('optional-dep-test@1.1', Spec('b')))

        self.check_normalize('optional-dep-test%intel',
                             Spec('optional-dep-test%intel', Spec('c')))

        self.check_normalize('optional-dep-test%intel@64.1',
                             Spec('optional-dep-test%intel@64.1', Spec('c'), Spec('d')))

        self.check_normalize('optional-dep-test%intel@64.1.2',
                             Spec('optional-dep-test%intel@64.1.2', Spec('c'), Spec('d')))

        self.check_normalize('optional-dep-test%clang@35',
                             Spec('optional-dep-test%clang@35', Spec('e')))


    def test_multiple_conditionals(self):
        self.check_normalize('optional-dep-test+a@1.1',
                             Spec('optional-dep-test+a@1.1', Spec('a'), Spec('b')))

        self.check_normalize('optional-dep-test+a%intel',
                             Spec('optional-dep-test+a%intel', Spec('a'), Spec('c')))

        self.check_normalize('optional-dep-test@1.1%intel',
                             Spec('optional-dep-test@1.1%intel', Spec('b'), Spec('c')))

        self.check_normalize('optional-dep-test@1.1%intel@64.1.2+a',
                             Spec('optional-dep-test@1.1%intel@64.1.2+a',
                                  Spec('b'), Spec('a'), Spec('c'), Spec('d')))

        self.check_normalize('optional-dep-test@1.1%clang@36.5+a',
                             Spec('optional-dep-test@1.1%clang@36.5+a',
                                  Spec('b'), Spec('a'), Spec('e')))


    def test_chained_mpi(self):
        self.check_normalize('optional-dep-test-2+mpi',
                             Spec('optional-dep-test-2+mpi',
                                  Spec('optional-dep-test+mpi',
                                       Spec('mpi'))))


    def test_default_variant(self):
        spec = Spec('optional-dep-test-3')
        spec.concretize()
        self.assertTrue('a' in spec)

        spec = Spec('optional-dep-test-3~var')
        spec.concretize()
        self.assertTrue('a' in spec)

        spec = Spec('optional-dep-test-3+var')
        spec.concretize()
        self.assertTrue('b' in spec)


    def test_transitive_chain(self):
        # Each of these dependencies comes from a conditional
        # dependency on another.  This requires iterating to evaluate
        # the whole chain.
        self.check_normalize(
            'optional-dep-test+f',
            Spec('optional-dep-test+f', Spec('f'), Spec('g'), Spec('mpi')))
