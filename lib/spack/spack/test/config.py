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
import shutil
import os
from tempfile import mkdtemp
import spack
from spack.packages import PackageDB
from spack.test.mock_packages_test import *

class ConfigTest(MockPackagesTest):

    def setUp(self):
        self.initmock()
        self.tmp_dir = mkdtemp('.tmp', 'spack-config-test-')
        spack.config.config_scopes = [('test_low_priority', os.path.join(self.tmp_dir, 'low')),
                                      ('test_high_priority', os.path.join(self.tmp_dir, 'high'))]

    def tearDown(self):
        self.cleanmock()
        shutil.rmtree(self.tmp_dir, True)

    def check_config(self, comps):
        config = spack.config.get_compilers_config()
        compiler_list = ['cc', 'cxx', 'f77', 'f90']
        for key in comps:
            for c in compiler_list:
                if comps[key][c] == '/bad':
                    continue
                self.assertEqual(comps[key][c], config[key][c])


    def test_write_key(self):
        a_comps =  {"gcc@4.7.3" : { "cc" : "/gcc473", "cxx" : "/g++473", "f77" : None, "f90" : None },
         "gcc@4.5.0" : { "cc" : "/gcc450", "cxx" : "/g++450", "f77" : "/gfortran", "f90" : "/gfortran" },
         "clang@3.3"  : { "cc" : "/bad", "cxx" : "/bad", "f77" : "/bad", "f90" : "/bad" }}

        b_comps = {"icc@10.0" : { "cc" : "/icc100", "cxx" : "/icc100", "f77" : None, "f90" : None },
         "icc@11.1" : { "cc" : "/icc111", "cxx" : "/icp111", "f77" : "/ifort", "f90" : "/ifort" },
         "clang@3.3" : { "cc" : "/clang", "cxx" : "/clang++", "f77" :  None, "f90" : None}}

        spack.config.add_to_compiler_config(a_comps, 'test_low_priority')
        spack.config.add_to_compiler_config(b_comps, 'test_high_priority')

        self.check_config(a_comps)
        self.check_config(b_comps)

        spack.config.clear_config_caches()

        self.check_config(a_comps)
        self.check_config(b_comps)

