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
import os
import shutil
from tempfile import mkdtemp

import spack
import spack.config
from ordereddict_backport import OrderedDict
from spack.test.mock_packages_test import *

# Some sample compiler config data
a_comps =  {
    'gcc473': {
        'paths': {
            "cc" : "/gcc473",
            "cxx": "/g++473",
            "f77": None,
            "fc" : None 
            },
        'modules': None,
        'spec': 'gcc@4.7.3',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        },
    'gcc450': {
        'paths': {
            "cc" : "/gcc450",
            "cxx": "/g++450",
            "f77": 'gfortran',
            "fc" : 'gfortran'
            },
        'modules': None,
        'spec': 'gcc@4.5.0',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        },
    'clang33': {
        'paths': {
            "cc" : "<overwritten>",
            "cxx": "<overwritten>",
            "f77": '<overwritten>',
            "fc" : '<overwritten>' },
        'modules': None,
        'spec': 'clang@3.3',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        }
}

b_comps = {
    'icc100': {
        'paths': {
            "cc" : "/icc100",
            "cxx": "/icp100",
            "f77": None,
            "fc" : None
            },
        'modules': None,
        'spec': 'icc@10.0',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        },
    'icc111': {
        'paths': {
            "cc" : "/icc111",
            "cxx": "/icp111",
            "f77": 'ifort',
            "fc" : 'ifort'
            },
        'modules': None,
        'spec': 'icc@11.1',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        },
    'clang33': {
        'paths': {
            "cc" : "<overwritten>",
            "cxx": "<overwritten>",
            "f77": '<overwritten>',
            "fc" : '<overwritten>' },
        'modules': None,
        'spec': 'clang@3.3',
        'operating_system': {
            'name': 'CNL',
            'version': '10'
            }
        }
}

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


    def check_config(self, comps, *compiler_names):
        """Check that named compilers in comps match Spack's config."""
        config = spack.config.get_config('compilers')
        compiler_list = ['cc', 'cxx', 'f77', 'fc']
        param_list = ['modules', 'paths', 'spec', 'operating_system']
        for alias, compiler in config.items():
            if compiler['spec'] in compiler_names:
                for p in param_list:
                    expected = comps[alias][p]
                    actual = config[alias][p]
                    self.assertEqual(expected, actual)
                for c in compiler_list:
                    expected = comps[alias]['paths'][c]
                    actual = config[alias]['paths'][c]
                    self.assertEqual(expected, actual)

    def test_write_key_in_memory(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config('compilers', a_comps, 'test_low_priority')
        spack.config.update_config('compilers', b_comps, 'test_high_priority')

        # Make sure the config looks how we expect.
        self.check_config(a_comps, 'gcc@4.7.3', 'gcc@4.5.0')
        self.check_config(b_comps, 'icc@10.0', 'icc@11.1', 'clang@3.3')


    def test_write_key_to_disk(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config('compilers', a_comps, 'test_low_priority')
        spack.config.update_config('compilers', b_comps, 'test_high_priority')

        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()

        # Same check again, to ensure consistency.
        self.check_config(a_comps, 'gcc@4.7.3', 'gcc@4.5.0')
        self.check_config(b_comps, 'icc@10.0', 'icc@11.1', 'clang@3.3')
