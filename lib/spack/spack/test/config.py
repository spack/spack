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
from tempfile import mkdtemp

import spack
import spack.config
from ordereddict_backport import OrderedDict
from spack.test.mock_packages_test import *

# Some sample compiler config data
a_comps =  {
    "x86_64_E5v2_IntelIB": {
        "gcc@4.7.3" : {
            "cc" : "/gcc473",
            "cxx": "/g++473",
            "f77": None,
            "fc" : None },
        "gcc@4.5.0" : {
            "cc" : "/gcc450",
            "cxx": "/g++450",
            "f77": "/gfortran",
            "fc" : "/gfortran" },
        "clang@3.3"  : {
            "cc" : "<overwritten>",
            "cxx": "<overwritten>",
            "f77": "<overwritten>",
            "fc" : "<overwritten>" }
    }
}

b_comps = {
    "x86_64_E5v3": {
        "icc@10.0" : {
            "cc" : "/icc100",
            "cxx": "/icc100",
            "f77": None,
            "fc" : None },
        "icc@11.1" : {
            "cc" : "/icc111",
            "cxx": "/icp111",
            "f77": "/ifort",
            "fc" : "/ifort" },
        "clang@3.3" : {
            "cc" : "/clang",
            "cxx": "/clang++",
            "f77": None,
            "fc" : None}
    }
}

# Some Sample repo data
repos_low = [ "/some/path" ]
repos_high = [ "/some/other/path" ]

class ConfigTest(MockPackagesTest):

    def setUp(self):
        super(ConfigTest, self).setUp()
        self.tmp_dir = mkdtemp('.tmp', 'spack-config-test-')
        spack.config.config_scopes = OrderedDict()
        spack.config.ConfigScope('test_low_priority', os.path.join(self.tmp_dir, 'low'))
        spack.config.ConfigScope('test_high_priority', os.path.join(self.tmp_dir, 'high'))

    def tearDown(self):
        super(ConfigTest, self).tearDown()
        shutil.rmtree(self.tmp_dir, True)

    def check_config(self, comps, arch, *compiler_names):
        """Check that named compilers in comps match Spack's config."""
        config = spack.config.get_config('compilers')
        compiler_list = ['cc', 'cxx', 'f77', 'fc']
        for key in compiler_names:
            for c in compiler_list:
                expected = comps[arch][key][c]
                actual = config[arch][key][c]
                self.assertEqual(expected, actual)

    def test_write_list_in_memory(self):
        spack.config.update_config('repos', repos_low, 'test_low_priority')
        spack.config.update_config('repos', repos_high, 'test_high_priority')
        config = spack.config.get_config('repos')
        self.assertEqual(config, repos_high+repos_low)

    def test_write_key_in_memory(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config('compilers', a_comps, 'test_low_priority')
        spack.config.update_config('compilers', b_comps, 'test_high_priority')

        # Make sure the config looks how we expect.
        self.check_config(a_comps, 'x86_64_E5v2_IntelIB', 'gcc@4.7.3', 'gcc@4.5.0')
        self.check_config(b_comps, 'x86_64_E5v3', 'icc@10.0', 'icc@11.1', 'clang@3.3')

    def test_write_key_to_disk(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config('compilers', a_comps, 'test_low_priority')
        spack.config.update_config('compilers', b_comps, 'test_high_priority')

        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()

        # Same check again, to ensure consistency.
        self.check_config(a_comps, 'x86_64_E5v2_IntelIB', 'gcc@4.7.3', 'gcc@4.5.0')
        self.check_config(b_comps, 'x86_64_E5v3', 'icc@10.0', 'icc@11.1', 'clang@3.3')

    def test_write_to_same_priority_file(self):
        # Write b_comps in the same file as a_comps.
        spack.config.update_config('compilers', a_comps, 'test_low_priority')
        spack.config.update_config('compilers', b_comps, 'test_low_priority')

        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()

        # Same check again, to ensure consistency.
        self.check_config(a_comps, 'x86_64_E5v2_IntelIB', 'gcc@4.7.3', 'gcc@4.5.0')
        self.check_config(b_comps, 'x86_64_E5v3', 'icc@10.0', 'icc@11.1', 'clang@3.3')
