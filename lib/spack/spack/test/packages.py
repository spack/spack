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

from llnl.util.filesystem import join_path

import spack
import spack.packages as packages
from spack.util.naming import mod_to_class
from spack.test.mock_packages_test import *


class PackagesTest(MockPackagesTest):

    def test_load_package(self):
        pkg = spack.db.get('mpich')


    def test_package_name(self):
        pkg = spack.db.get('mpich')
        self.assertEqual(pkg.name, 'mpich')


    def test_package_filename(self):
        filename = spack.db.filename_for_package_name('mpich')
        self.assertEqual(filename, join_path(spack.mock_packages_path, 'mpich', 'package.py'))


    def test_package_name(self):
        pkg = spack.db.get('mpich')
        self.assertEqual(pkg.name, 'mpich')


    def test_nonexisting_package_filename(self):
        filename = spack.db.filename_for_package_name('some-nonexisting-package')
        self.assertEqual(filename, join_path(spack.mock_packages_path, 'some-nonexisting-package', 'package.py'))


    def test_package_class_names(self):
        self.assertEqual('Mpich',          mod_to_class('mpich'))
        self.assertEqual('PmgrCollective', mod_to_class('pmgr_collective'))
        self.assertEqual('PmgrCollective', mod_to_class('pmgr-collective'))
        self.assertEqual('Pmgrcollective', mod_to_class('PmgrCollective'))
        self.assertEqual('_3db',        mod_to_class('3db'))
