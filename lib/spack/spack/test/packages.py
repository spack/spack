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

from spack.test.mock_packages_test import *
import spack.packages as packages

class PackagesTest(MockPackagesTest):

    def test_load_regular_package(self):
        pkg = packages.get('mpich')


    def test_regular_package_name(self):
        pkg = packages.get('mpich')
        self.assertEqual(pkg.name, 'mpich')


    def test_regular_package_filename(self):
        filename = packages.filename_for_package_name('mpich')
        self.assertEqual(filename, new_path(mock_packages_path, 'mpich.py'))


    def test_regular_package_name(self):
        pkg = packages.get('mpich')
        self.assertEqual(pkg.name, 'mpich')


    def test_load_directory_package(self):
        pkg = packages.get('directory-pkg')
        self.assertTrue(hasattr(pkg, 'this_is_a_directory_pkg'))
        self.assertTrue(pkg.this_is_a_directory_pkg)


    def test_directory_package_name(self):
        pkg = packages.get('directory-pkg')
        self.assertEqual(pkg.name, 'directory-pkg')


    def test_directory_package_filename(self):
        filename = packages.filename_for_package_name('directory-pkg')
        self.assertEqual(filename, new_path(mock_packages_path, 'directory-pkg/__init__.py'))


    def test_nonexisting_package_filename(self):
        filename = packages.filename_for_package_name('some-nonexisting-package')
        self.assertEqual(filename, new_path(mock_packages_path, 'some-nonexisting-package.py'))
