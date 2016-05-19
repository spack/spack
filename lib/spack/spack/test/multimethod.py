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
"""
Test for multi_method dispatch.
"""
import unittest

import spack
from spack.multimethod import *
from spack.version import *
from spack.spec import Spec
from spack.multimethod import when
from spack.test.mock_packages_test import *
from spack.version import *


class MultiMethodTest(MockPackagesTest):

    def test_no_version_match(self):
        pkg = spack.repo.get('multimethod@2.0')
        self.assertRaises(NoSuchMethodError, pkg.no_version_2)


    def test_one_version_match(self):
        pkg = spack.repo.get('multimethod@1.0')
        self.assertEqual(pkg.no_version_2(), 1)

        pkg = spack.repo.get('multimethod@3.0')
        self.assertEqual(pkg.no_version_2(), 3)

        pkg = spack.repo.get('multimethod@4.0')
        self.assertEqual(pkg.no_version_2(), 4)


    def test_version_overlap(self):
        pkg = spack.repo.get('multimethod@2.0')
        self.assertEqual(pkg.version_overlap(), 1)

        pkg = spack.repo.get('multimethod@5.0')
        self.assertEqual(pkg.version_overlap(), 2)


    def test_mpi_version(self):
        pkg = spack.repo.get('multimethod^mpich@3.0.4')
        self.assertEqual(pkg.mpi_version(), 3)

        pkg = spack.repo.get('multimethod^mpich2@1.2')
        self.assertEqual(pkg.mpi_version(), 2)

        pkg = spack.repo.get('multimethod^mpich@1.0')
        self.assertEqual(pkg.mpi_version(), 1)


    def test_undefined_mpi_version(self):
        pkg = spack.repo.get('multimethod^mpich@0.4')
        self.assertEqual(pkg.mpi_version(), 1)

        pkg = spack.repo.get('multimethod^mpich@1.4')
        self.assertEqual(pkg.mpi_version(), 1)


    def test_default_works(self):
        pkg = spack.repo.get('multimethod%gcc')
        self.assertEqual(pkg.has_a_default(), 'gcc')

        pkg = spack.repo.get('multimethod%intel')
        self.assertEqual(pkg.has_a_default(), 'intel')

        pkg = spack.repo.get('multimethod%pgi')
        self.assertEqual(pkg.has_a_default(), 'default')


    def test_architecture_match(self):
        pkg = spack.repo.get('multimethod arch=x86_64')
        self.assertEqual(pkg.different_by_architecture(), 'x86_64')

        pkg = spack.repo.get('multimethod arch=ppc64')
        self.assertEqual(pkg.different_by_architecture(), 'ppc64')

        pkg = spack.repo.get('multimethod arch=ppc32')
        self.assertEqual(pkg.different_by_architecture(), 'ppc32')

        pkg = spack.repo.get('multimethod arch=arm64')
        self.assertEqual(pkg.different_by_architecture(), 'arm64')

        pkg = spack.repo.get('multimethod arch=macos')
        self.assertRaises(NoSuchMethodError, pkg.different_by_architecture)


    def test_dependency_match(self):
        pkg = spack.repo.get('multimethod^zmpi')
        self.assertEqual(pkg.different_by_dep(), 'zmpi')

        pkg = spack.repo.get('multimethod^mpich')
        self.assertEqual(pkg.different_by_dep(), 'mpich')

        # If we try to switch on some entirely different dep, it's ambiguous,
        # but should take the first option
        pkg = spack.repo.get('multimethod^foobar')
        self.assertEqual(pkg.different_by_dep(), 'mpich')


    def test_virtual_dep_match(self):
        pkg = spack.repo.get('multimethod^mpich2')
        self.assertEqual(pkg.different_by_virtual_dep(), 2)

        pkg = spack.repo.get('multimethod^mpich@1.0')
        self.assertEqual(pkg.different_by_virtual_dep(), 1)
