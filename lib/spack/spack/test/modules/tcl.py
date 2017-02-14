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
import spack.modules.tcl
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
            spack.modules.tcl,
            'configuration',
            configuration['tcl']
        )
        monkeypatch.setattr(
            spack.modules.tcl,
            'configuration_registry',
            {}
        )
    return _impl


@pytest.fixture()
def tcl_modulefile(modulefile_content):
    return functools.partial(
        modulefile_content, spack.modules.tcl.TclModulefileWriter
    )


@pytest.fixture()
def tcl_factory():
    return spack.modules.tcl.TclModulefileWriter


@pytest.mark.usefixtures('config', 'builtin_mock')
class TestTcl(object):

    configuration_autoload_direct = {
        'enable': ['tcl'],
        'tcl': {
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_autoload_all = {
        'enable': ['tcl'],
        'tcl': {
            'all': {
                'autoload': 'all'
            }
        }
    }

    configuration_prerequisites_direct = {
        'enable': ['tcl'],
        'tcl': {
            'all': {
                'prerequisites': 'direct'
            }
        }
    }

    configuration_prerequisites_all = {
        'enable': ['tcl'],
        'tcl': {
            'all': {
                'prerequisites': 'all'
            }
        }
    }

    configuration_alter_environment = {
        'enable': ['tcl'],
        'tcl': {
            'all': {
                'filter': {'environment_blacklist': ['CMAKE_PREFIX_PATH']},
                'environment': {
                    'set': {'${PACKAGE}_ROOT': '${PREFIX}'}
                }
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
        'enable': ['tcl'],
        'tcl': {
            'whitelist': ['zmpi'],
            'blacklist': ['callpath', 'mpi'],
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_conflicts = {
        'enable': ['tcl'],
        'tcl': {
            'naming_scheme': '${PACKAGE}/${VERSION}-${COMPILERNAME}',
            'all': {
                'conflict': ['${PACKAGE}', 'intel/14.0.1']
            }
        }
    }

    configuration_wrong_conflicts = {
        'enable': ['tcl'],
        'tcl': {
            'naming_scheme': '${PACKAGE}/${VERSION}-${COMPILERNAME}',
            'all': {
                'conflict': ['${PACKAGE}/${COMPILERNAME}']
            }
        }
    }

    configuration_suffix = {
        'enable': ['tcl'],
        'tcl': {
            'mpileaks': {
                'suffixes': {
                    '+debug': 'foo',
                    '~debug': 'bar'
                }
            }
        }
    }

    def test_simple_case(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_direct)
        content = tcl_modulefile(mpich_spec_string)
        assert 'module-whatis "mpich @3.0.4"' in content

    def test_autoload_direct(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_direct)
        content = tcl_modulefile(mpileaks_spec_string)
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = tcl_modulefile('dtbuild1')
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

    def test_autoload_all(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_autoload_all)
        content = tcl_modulefile(mpileaks_spec_string)
        assert len([x for x in content if 'is-loaded' in x]) == 5
        assert len([x for x in content if 'module load ' in x]) == 5

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = tcl_modulefile('dtbuild1')
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

    def test_prerequisites_direct(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_prerequisites_direct)
        content = tcl_modulefile('mpileaks arch=x86-linux')
        assert len([x for x in content if 'prereq' in x]) == 2

    def test_prerequisites_all(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_prerequisites_all)
        content = tcl_modulefile('mpileaks arch=x86-linux')
        assert len([x for x in content if 'prereq' in x]) == 5

    def test_alter_environment(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_alter_environment)
        content = tcl_modulefile('mpileaks platform=test target=x86_64')
        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 1
        assert len([x for x in content if 'unsetenv BAR' in x]) == 1
        assert len([x for x in content if 'setenv MPILEAKS_ROOT' in x]) == 1

        content = tcl_modulefile('libdwarf %clang platform=test target=x86_32')
        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 0
        assert len([x for x in content if 'is-loaded foo/bar' in x]) == 1
        assert len([x for x in content if 'module load foo/bar' in x]) == 1
        assert len([x for x in content if 'setenv LIBDWARF_ROOT' in x]) == 1

    def test_blacklist(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_blacklist)
        content = tcl_modulefile('mpileaks ^zmpi')
        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1
        # Returns a StringIO instead of a string as no module file was written
        with pytest.raises(AttributeError):
            tcl_modulefile('callpath arch=x86-linux')
        content = tcl_modulefile('zmpi arch=x86-linux')
        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

    def test_conflicts(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_conflicts)
        content = tcl_modulefile('mpileaks')
        assert len([x for x in content if x.startswith('conflict')]) == 2
        assert len([x for x in content if x == 'conflict mpileaks']) == 1
        assert len([x for x in content if x == 'conflict intel/14.0.1']) == 1

    def test_wrong_conflicts(self, tcl_modulefile, patch_configuration):
        patch_configuration(self.configuration_wrong_conflicts)
        with pytest.raises(SystemExit):
            tcl_modulefile('mpileaks')

    def test_suffixes(self, tcl_factory, patch_configuration):
        patch_configuration(self.configuration_suffix)
        spec = spack.spec.Spec('mpileaks+debug arch=x86-linux')
        spec.concretize()
        generator = tcl_factory(spec)
        assert 'foo' in generator.layout.use_name

        spec = spack.spec.Spec('mpileaks~debug arch=x86-linux')
        spec.concretize()
        generator = tcl_factory(spec)
        assert 'bar' in generator.layout.use_name

    def test_setup_environment(self, tcl_modulefile):
        patch_configuration(self.configuration_suffix)
        content = tcl_modulefile('mpileaks')
        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "mpileaks"' in x]
        ) == 1

        spec = spack.spec.Spec('mpileaks')
        spec.concretize()
        content = tcl_modulefile(str(spec['callpath']))
        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "callpath"' in x]
        ) == 1
