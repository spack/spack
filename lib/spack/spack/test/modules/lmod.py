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

import functools

import pytest
import spack.modules.common
import spack.modules.lmod
import spack.spec

mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf arch=x64-linux'


@pytest.fixture()
def patch_configuration(monkeypatch):
    def _impl(configuration):
        monkeypatch.setattr(
            spack.modules.common,
            'configuration',
            configuration
        )
        monkeypatch.setattr(
            spack.modules.lmod,
            'configuration',
            configuration['lmod']
        )
        monkeypatch.setattr(
            spack.modules.lmod,
            'configuration_registry',
            {}
        )
    return _impl


@pytest.fixture()
def lmod_modulefile(modulefile_content):
    return functools.partial(
        modulefile_content, spack.modules.lmod.LmodModulefileWriter
    )


@pytest.fixture()
def lmod_factory():

    def _mock(spec_string):
        spec = spack.spec.Spec(spec_string)
        spec.concretize()
        factory = spack.modules.lmod.LmodModulefileWriter
        return factory(spec), spec

    return _mock


@pytest.fixture(params=[
    'clang@3.3',
    'gcc@4.5.0'
])
def compiler(request):
    return request.param


@pytest.fixture(params=[
    ('mpich@3.0.4', ('mpi',)),
    ('openblas@0.2.15', ('blas',)),
    ('openblas-with-lapack@0.2.15', ('blas', 'lapack'))
])
def provider(request):
    return request.param


@pytest.mark.usefixtures('config', 'builtin_mock',)
class TestLmod(object):
    configuration_complex_hierarchy = {
        'enable': ['lmod'],
        'lmod': {
            'hash_length': 0,
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['lapack', 'blas', 'mpi'],
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_autoload_direct = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_autoload_all = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'verbose': False,
            'all': {
                'autoload': 'all'
            }
        }
    }

    configuration_no_hash = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'hash_length': 0
        }
    }

    configuration_alter_environment = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'all': {
                'filter': {'environment_blacklist': ['CMAKE_PREFIX_PATH']}
            },
            'platform=test target=x86_64': {
                'environment': {
                    'set': {'FOO': 'foo'},
                    'unset': ['BAR']
                }
            },
            'platform=test target=x86_32': {
                'load': ['foo/bar']
            }
        }
    }

    configuration_blacklist = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'blacklist': ['callpath'],
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_override = {
        'enable': ['lmod'],
        'lmod': {
            'core_compilers': ['clang@3.3'],
            'hierarchy': ['mpi'],
            'all': {
                'template': 'override_from_modules.txt'
            }
        }
    }

    def test_file_layout(
            self, compiler, provider, lmod_factory, patch_configuration
    ):
        patch_configuration(self.configuration_complex_hierarchy)
        spec_string, services = provider
        module, spec = lmod_factory(spec_string + '%' + compiler)

        layout = module.layout

        # Check that the services provided are in the hierarchy
        for s in services:
            assert s in layout.conf.hierarchy_tokens

        # Check that the compiler part of the path has no hash and that it
        # is transformed to r"Core" if the compiler is listed among core
        # compilers
        if compiler == 'clang@3.3':
            assert 'Core' in layout.available_path_parts
        else:
            assert compiler.replace('@', '/') in layout.available_path_parts

        # Check that the provider part instead has always an hash even if
        # hash has been disallowed in the configuration file
        path_parts = layout.available_path_parts
        service_part = spec_string.replace('@', '/')
        service_part = '-'.join([service_part, layout.spec.dag_hash(length=7)])
        assert service_part in path_parts

        # Check that multi-providers have repetitions in path parts
        repetitions = len([x for x in path_parts if service_part == x])
        if spec_string == 'openblas-with-lapack@0.2.15':
            assert repetitions == 2
        else:
            assert repetitions == 1

    def test_simple_case(self, lmod_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_direct)
        content = lmod_modulefile(mpich_spec_string)
        assert '-- -*- lua -*-' in content
        assert 'whatis([[Name : mpich]])' in content
        assert 'whatis([[Version : 3.0.4]])' in content
        assert 'family("mpi")' in content

    def test_autoload_direct(self, lmod_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_direct)
        content = lmod_modulefile(mpileaks_spec_string)
        assert len([x for x in content if 'if not isloaded(' in x]) == 2
        assert len([x for x in content if 'load(' in x]) == 2
        # The configuration file doesn't set the verbose keyword
        # that defaults to True
        messages = [x for x in content if 'LmodMessage("Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, lmod_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_all)
        content = lmod_modulefile(mpileaks_spec_string)
        assert len([x for x in content if 'if not isloaded(' in x]) == 5
        assert len([x for x in content if 'load(' in x]) == 5
        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'LmodMessage("Autoloading' in x]
        assert len(messages) == 0

    def test_alter_environment(self, lmod_modulefile, patch_configuration):
        patch_configuration(self.configuration_alter_environment)
        content = lmod_modulefile('mpileaks platform=test target=x86_64')
        assert len(
            [x for x in content if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 1
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 1

        content = lmod_modulefile(
            'libdwarf %clang platform=test target=x86_32'
        )
        assert len(
            [x for x in content if x.startswith('prepend-path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 0
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 0

    def test_blacklist(self, lmod_modulefile, patch_configuration):
        patch_configuration(self.configuration_blacklist)
        content = lmod_modulefile(mpileaks_spec_string)
        assert len([x for x in content if 'if not isloaded(' in x]) == 1
        assert len([x for x in content if 'load(' in x]) == 1

    def test_no_hash(self, lmod_factory, patch_configuration):
        # Make sure that virtual providers (in the hierarchy) always
        # include a hash. Make sure that the module file for the spec
        # does not include a hash if hash_length is 0.
        patch_configuration(self.configuration_no_hash)
        module, spec = lmod_factory(mpileaks_spec_string)
        path = module.layout.filename
        mpi_spec = spec['mpi']
        mpiElement = "{0}/{1}-{2}/".format(
            mpi_spec.name, mpi_spec.version, mpi_spec.dag_hash(length=7)
        )
        assert mpiElement in path
        mpileaks_spec = spec
        mpileaks_element = "{0}/{1}.lua".format(
            mpileaks_spec.name, mpileaks_spec.version
        )
        assert path.endswith(mpileaks_element)

    @pytest.mark.usefixtures('update_template_dirs')
    def test_override_template_in_package(
            self, lmod_modulefile, patch_configuration
    ):
        """Tests overriding a template reading an attribute in the package."""
        patch_configuration(self.configuration_autoload_direct)
        content = lmod_modulefile('override-module-templates')
        assert 'Override successful!' in content

    @pytest.mark.usefixtures('update_template_dirs')
    def test_override_template_in_modules_yaml(
            self, lmod_modulefile, patch_configuration
    ):
        """Tests overriding a template reading `modules.yaml`"""
        patch_configuration(self.configuration_override)

        content = lmod_modulefile('override-module-templates')
        assert 'Override even better!' in content

        content = lmod_modulefile('mpileaks arch=x86-linux')
        assert 'Override even better!' in content
