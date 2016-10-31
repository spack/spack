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
import getpass
import yaml
from tempfile import mkdtemp

import spack
import spack.config
from spack.util.path import canonicalize_path
from ordereddict_backport import OrderedDict
from spack.test.mock_packages_test import *

# Some sample compiler config data
a_comps = {
    'compilers': [
        {'compiler': {
            'paths': {
                "cc": "/gcc473",
                "cxx": "/g++473",
                "f77": None,
                "fc": None
            },
            'modules': None,
            'spec': 'gcc@4.7.3',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "/gcc450",
                "cxx": "/g++450",
                "f77": 'gfortran',
                "fc": 'gfortran'
            },
            'modules': None,
            'spec': 'gcc@4.5.0',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "/gcc422",
                "cxx": "/g++422",
                "f77": 'gfortran',
                "fc": 'gfortran'
            },
            'flags': {
                "cppflags": "-O0 -fpic",
                "fflags": "-f77",
            },
            'modules': None,
            'spec': 'gcc@4.2.2',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "<overwritten>",
                "cxx": "<overwritten>",
                "f77": '<overwritten>',
                "fc": '<overwritten>'},
            'modules': None,
            'spec': 'clang@3.3',
            'operating_system': 'CNL10'
        }}
    ]
}

b_comps = {
    'compilers': [
        {'compiler': {
            'paths': {
                "cc": "/icc100",
                "cxx": "/icp100",
                "f77": None,
                "fc": None
            },
            'modules': None,
            'spec': 'icc@10.0',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "/icc111",
                "cxx": "/icp111",
                "f77": 'ifort',
                "fc": 'ifort'
            },
            'modules': None,
            'spec': 'icc@11.1',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "/icc123",
                "cxx": "/icp123",
                "f77": 'ifort',
                "fc": 'ifort'
            },
            'flags': {
                "cppflags": "-O3",
                "fflags": "-f77rtl",
            },
            'modules': None,
            'spec': 'icc@12.3',
            'operating_system': 'CNL10'
        }},
        {'compiler': {
            'paths': {
                "cc": "<overwritten>",
                "cxx": "<overwritten>",
                "f77": '<overwritten>',
                "fc": '<overwritten>'},
            'modules': None,
            'spec': 'clang@3.3',
            'operating_system': 'CNL10'
        }}
    ]
}

# Some Sample repo data
repos_low = {'repos': ["/some/path"]}
repos_high = {'repos': ["/some/other/path"]}


# sample config data
config_low = {
    'config': {
        'install_tree': 'install_tree_path',
        'build_stage': ['path1', 'path2', 'path3']}}

config_override_all = {
    'config:': {
        'install_tree:': 'override_all'}}

config_override_key = {
    'config': {
        'install_tree:': 'override_key'}}

config_merge_list = {
    'config': {
        'build_stage': ['patha', 'pathb']}}

config_override_list = {
    'config': {
        'build_stage:': ['patha', 'pathb']}}


class ConfigTest(MockPackagesTest):

    def setUp(self):
        super(ConfigTest, self).setUp()
        self.tmp_dir = mkdtemp('.tmp', 'spack-config-test-')
        self.a_comp_specs = [
            ac['compiler']['spec'] for ac in a_comps['compilers']]
        self.b_comp_specs = [
            bc['compiler']['spec'] for bc in b_comps['compilers']]

        spack.config.config_scopes = OrderedDict()
        for priority in ['low', 'high']:
            scope_dir = os.path.join(self.tmp_dir, priority)
            spack.config.ConfigScope(priority, scope_dir)

    def tearDown(self):
        super(ConfigTest, self).tearDown()
        shutil.rmtree(self.tmp_dir, True)

    def write_config_file(self, config, data, scope):
        scope_dir = os.path.join(self.tmp_dir, scope)
        mkdirp(scope_dir)

        path = os.path.join(scope_dir, config + '.yaml')
        with open(path, 'w') as f:
            print yaml
            yaml.dump(data, f)

    def check_compiler_config(self, comps, *compiler_names):
        """Check that named compilers in comps match Spack's config."""
        config = spack.config.get_config('compilers')
        compiler_list = ['cc', 'cxx', 'f77', 'fc']
        flag_list = ['cflags', 'cxxflags', 'fflags', 'cppflags',
                     'ldflags', 'ldlibs']
        param_list = ['modules', 'paths', 'spec', 'operating_system']
        for compiler in config:
            conf = compiler['compiler']
            if conf['spec'] in compiler_names:
                comp = next((c['compiler'] for c in comps if
                             c['compiler']['spec'] == conf['spec']), None)
                if not comp:
                    self.fail('Bad config spec')
                for p in param_list:
                    self.assertEqual(conf[p], comp[p])
                for f in flag_list:
                    expected = comp.get('flags', {}).get(f, None)
                    actual = conf.get('flags', {}).get(f, None)
                    self.assertEqual(expected, actual)
                for c in compiler_list:
                    expected = comp['paths'][c]
                    actual = conf['paths'][c]
                    self.assertEqual(expected, actual)

    def test_write_list_in_memory(self):
        spack.config.update_config('repos', repos_low['repos'], scope='low')
        spack.config.update_config('repos', repos_high['repos'], scope='high')

        config = spack.config.get_config('repos')
        self.assertEqual(config, repos_high['repos'] + repos_low['repos'])

    def test_write_key_in_memory(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low')
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='high')

        # Make sure the config looks how we expect.
        self.check_compiler_config(a_comps['compilers'], *self.a_comp_specs)
        self.check_compiler_config(b_comps['compilers'], *self.b_comp_specs)

    def test_write_key_to_disk(self):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low')
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='high')

        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()

        # Same check again, to ensure consistency.
        self.check_compiler_config(a_comps['compilers'], *self.a_comp_specs)
        self.check_compiler_config(b_comps['compilers'], *self.b_comp_specs)

    def test_write_to_same_priority_file(self):
        # Write b_comps in the same file as a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low')
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='low')

        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()

        # Same check again, to ensure consistency.
        self.check_compiler_config(a_comps['compilers'], *self.a_comp_specs)
        self.check_compiler_config(b_comps['compilers'], *self.b_comp_specs)

    def check_canonical(self, var, expected):
        """Ensure that <expected> is substituted properly for <var> in strings
           containing <var> in various positions."""
        path = '/foo/bar/baz'

        self.assertEqual(canonicalize_path(var + path),
                         expected + path)

        self.assertEqual(canonicalize_path(path + var),
                         path + '/' + expected)

        self.assertEqual(canonicalize_path(path + var + path),
                         expected + path)

    def test_substitute_config_variables(self):
        prefix = spack.prefix.lstrip('/')

        self.assertEqual(os.path.join('/foo/bar/baz', prefix),
                         canonicalize_path('/foo/bar/baz/$spack'))

        self.assertEqual(os.path.join(spack.prefix, 'foo/bar/baz'),
                         canonicalize_path('$spack/foo/bar/baz/'))

        self.assertEqual(os.path.join('/foo/bar/baz', prefix, 'foo/bar/baz'),
                         canonicalize_path('/foo/bar/baz/$spack/foo/bar/baz/'))

        self.assertEqual(os.path.join('/foo/bar/baz', prefix),
                         canonicalize_path('/foo/bar/baz/${spack}'))

        self.assertEqual(os.path.join(spack.prefix, 'foo/bar/baz'),
                         canonicalize_path('${spack}/foo/bar/baz/'))

        self.assertEqual(
            os.path.join('/foo/bar/baz', prefix, 'foo/bar/baz'),
            canonicalize_path('/foo/bar/baz/${spack}/foo/bar/baz/'))

        self.assertNotEqual(
            os.path.join('/foo/bar/baz', prefix, 'foo/bar/baz'),
            canonicalize_path('/foo/bar/baz/${spack/foo/bar/baz/'))

    def test_substitute_user(self):
        user = getpass.getuser()
        self.assertEqual('/foo/bar/' + user + '/baz',
                         canonicalize_path('/foo/bar/$user/baz'))

    def test_substitute_tempdir(self):
        tempdir = tempfile.gettempdir()
        self.assertEqual(tempdir, canonicalize_path('$tempdir'))
        self.assertEqual(tempdir + '/foo/bar/baz',
                         canonicalize_path('$tempdir/foo/bar/baz'))

    def test_read_config(self):
        self.write_config_file('config', config_low, 'low')
        self.assertEqual(spack.config.get_config('config'),
                         config_low['config'])

    def test_read_config_override_all(self):
        self.write_config_file('config', config_low, 'low')
        self.write_config_file('config', config_override_all, 'high')
        self.assertEqual(spack.config.get_config('config'), {
            'install_tree': 'override_all'
        })

    def test_read_config_override_key(self):
        self.write_config_file('config', config_low, 'low')
        self.write_config_file('config', config_override_key, 'high')
        self.assertEqual(spack.config.get_config('config'), {
            'install_tree': 'override_key',
            'build_stage': ['path1', 'path2', 'path3']
        })

    def test_read_config_merge_list(self):
        self.write_config_file('config', config_low, 'low')
        self.write_config_file('config', config_merge_list, 'high')
        self.assertEqual(spack.config.get_config('config'), {
            'install_tree': 'install_tree_path',
            'build_stage': ['patha', 'pathb', 'path1', 'path2', 'path3']
        })

    def test_read_config_override_list(self):
        self.write_config_file('config', config_low, 'low')
        self.write_config_file('config', config_override_list, 'high')
        self.assertEqual(spack.config.get_config('config'), {
            'install_tree': 'install_tree_path',
            'build_stage': ['patha', 'pathb']
        })
