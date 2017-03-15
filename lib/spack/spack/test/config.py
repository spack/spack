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
import collections
import getpass
import os
import tempfile

import ordereddict_backport
import pytest
import spack
import spack.config
import yaml
from spack.util.path import canonicalize_path

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


def check_compiler_config(comps, *compiler_names):
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
                raise ValueError('Bad config spec')
            for p in param_list:
                assert conf[p] == comp[p]
            for f in flag_list:
                expected = comp.get('flags', {}).get(f, None)
                actual = conf.get('flags', {}).get(f, None)
                assert expected == actual
            for c in compiler_list:
                expected = comp['paths'][c]
                actual = conf['paths'][c]
                assert expected == actual


@pytest.fixture()
def config(tmpdir):
    """Mocks the configuration scope."""
    spack.config.clear_config_caches()
    real_scope = spack.config.config_scopes
    spack.config.config_scopes = ordereddict_backport.OrderedDict()
    for priority in ['low', 'high']:
        spack.config.ConfigScope(priority, str(tmpdir.join(priority)))
    Config = collections.namedtuple('Config', ['real', 'mock'])
    yield Config(real=real_scope, mock=spack.config.config_scopes)
    spack.config.config_scopes = real_scope
    spack.config.clear_config_caches()


@pytest.fixture()
def write_config_file(tmpdir):
    """Returns a function that writes a config file."""
    def _write(config, data, scope):
        config_yaml = tmpdir.join(scope, config + '.yaml')
        config_yaml.ensure()
        with config_yaml.open('w') as f:
            yaml.dump(data, f)
    return _write


@pytest.fixture()
def compiler_specs():
    """Returns a couple of compiler specs needed for the tests"""
    a = [ac['compiler']['spec'] for ac in a_comps['compilers']]
    b = [bc['compiler']['spec'] for bc in b_comps['compilers']]
    CompilerSpecs = collections.namedtuple('CompilerSpecs', ['a', 'b'])
    return CompilerSpecs(a=a, b=b)


@pytest.mark.usefixtures('config')
class TestConfig(object):

    def test_write_list_in_memory(self):
        spack.config.update_config('repos', repos_low['repos'], scope='low')
        spack.config.update_config('repos', repos_high['repos'], scope='high')

        config = spack.config.get_config('repos')
        assert config == repos_high['repos'] + repos_low['repos']

    def test_write_key_in_memory(self, compiler_specs):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low'
        )
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='high'
        )
        # Make sure the config looks how we expect.
        check_compiler_config(a_comps['compilers'], *compiler_specs.a)
        check_compiler_config(b_comps['compilers'], *compiler_specs.b)

    def test_write_key_to_disk(self, compiler_specs):
        # Write b_comps "on top of" a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low'
        )
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='high'
        )
        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()
        # Same check again, to ensure consistency.
        check_compiler_config(a_comps['compilers'], *compiler_specs.a)
        check_compiler_config(b_comps['compilers'], *compiler_specs.b)

    def test_write_to_same_priority_file(self, compiler_specs):
        # Write b_comps in the same file as a_comps.
        spack.config.update_config(
            'compilers', a_comps['compilers'], scope='low'
        )
        spack.config.update_config(
            'compilers', b_comps['compilers'], scope='low'
        )
        # Clear caches so we're forced to read from disk.
        spack.config.clear_config_caches()
        # Same check again, to ensure consistency.
        check_compiler_config(a_comps['compilers'], *compiler_specs.a)
        check_compiler_config(b_comps['compilers'], *compiler_specs.b)

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

        assert os.path.join(
            '/foo/bar/baz', prefix
        ) == canonicalize_path('/foo/bar/baz/$spack')

        assert os.path.join(
            spack.prefix, 'foo/bar/baz'
        ) == canonicalize_path('$spack/foo/bar/baz/')

        assert os.path.join(
            '/foo/bar/baz', prefix, 'foo/bar/baz'
        ) == canonicalize_path('/foo/bar/baz/$spack/foo/bar/baz/')

        assert os.path.join(
            '/foo/bar/baz', prefix
        ) == canonicalize_path('/foo/bar/baz/${spack}')

        assert os.path.join(
            spack.prefix, 'foo/bar/baz'
        ) == canonicalize_path('${spack}/foo/bar/baz/')

        assert os.path.join(
            '/foo/bar/baz', prefix, 'foo/bar/baz'
        ) == canonicalize_path('/foo/bar/baz/${spack}/foo/bar/baz/')

        assert os.path.join(
            '/foo/bar/baz', prefix, 'foo/bar/baz'
        ) != canonicalize_path('/foo/bar/baz/${spack/foo/bar/baz/')

    def test_substitute_user(self):
        user = getpass.getuser()
        assert '/foo/bar/' + user + '/baz' == canonicalize_path(
            '/foo/bar/$user/baz'
        )

    def test_substitute_tempdir(self):
        tempdir = tempfile.gettempdir()
        assert tempdir == canonicalize_path('$tempdir')
        assert tempdir + '/foo/bar/baz' == canonicalize_path(
            '$tempdir/foo/bar/baz'
        )

    def test_read_config(self, write_config_file):
        write_config_file('config', config_low, 'low')
        assert spack.config.get_config('config') == config_low['config']

    def test_read_config_override_all(self, write_config_file):
        write_config_file('config', config_low, 'low')
        write_config_file('config', config_override_all, 'high')
        assert spack.config.get_config('config') == {
            'install_tree': 'override_all'
        }

    def test_read_config_override_key(self, write_config_file):
        write_config_file('config', config_low, 'low')
        write_config_file('config', config_override_key, 'high')
        assert spack.config.get_config('config') == {
            'install_tree': 'override_key',
            'build_stage': ['path1', 'path2', 'path3']
        }

    def test_read_config_merge_list(self, write_config_file):
        write_config_file('config', config_low, 'low')
        write_config_file('config', config_merge_list, 'high')
        assert spack.config.get_config('config') == {
            'install_tree': 'install_tree_path',
            'build_stage': ['patha', 'pathb', 'path1', 'path2', 'path3']
        }

    def test_read_config_override_list(self, write_config_file):
        write_config_file('config', config_low, 'low')
        write_config_file('config', config_override_list, 'high')
        assert spack.config.get_config('config') == {
            'install_tree': 'install_tree_path',
            'build_stage': ['patha', 'pathb']
        }
