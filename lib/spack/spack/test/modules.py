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
import contextlib
from six import StringIO

import pytest
import spack.modules
import spack.spec

# Our "filesystem" for the tests below
FILE_REGISTRY = collections.defaultdict(StringIO)
# Spec strings that will be used throughout the tests
mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf arch=x64-linux'


@pytest.fixture()
def stringio_open(monkeypatch):
    """Overrides the `open` builtin in spack.modules with an implementation
    that writes on a StringIO instance.
    """
    @contextlib.contextmanager
    def _mock(filename, mode):
        if not mode == 'w':
            raise RuntimeError('unexpected opening mode for stringio_open')

        FILE_REGISTRY[filename] = StringIO()

        try:
            yield FILE_REGISTRY[filename]
        finally:
            handle = FILE_REGISTRY[filename]
            FILE_REGISTRY[filename] = handle.getvalue()
            handle.close()

    monkeypatch.setattr(spack.modules, 'open', _mock, raising=False)


def get_modulefile_content(factory, spec):
    """Writes the module file and returns the content as a string.

    :param factory: module file factory
    :param spec: spec of the module file to be written
    :return: content of the module file
    :rtype: str
    """
    spec.concretize()
    generator = factory(spec)
    generator.write()
    content = FILE_REGISTRY[generator.file_name].split('\n')
    generator.remove()
    return content


def test_update_dictionary_extending_list():
    target = {
        'foo': {
            'a': 1,
            'b': 2,
            'd': 4
        },
        'bar': [1, 2, 4],
        'baz': 'foobar'
    }
    update = {
        'foo': {
            'c': 3,
        },
        'bar': [3],
        'baz': 'foobaz',
        'newkey': {
            'd': 4
        }
    }
    spack.modules.update_dictionary_extending_lists(target, update)
    assert len(target) == 4
    assert len(target['foo']) == 4
    assert len(target['bar']) == 4
    assert target['baz'] == 'foobaz'


def test_inspect_path():
    env = spack.modules.inspect_path('/usr')
    names = [item.name for item in env]
    assert 'PATH' in names
    assert 'LIBRARY_PATH' in names
    assert 'LD_LIBRARY_PATH' in names
    assert 'CPATH' in names


@pytest.fixture()
def tcl_factory(tmpdir, monkeypatch):
    """Returns a factory that writes non-hierarchical TCL module files."""
    factory = spack.modules.TclModule
    monkeypatch.setattr(factory, 'path', str(tmpdir))
    monkeypatch.setattr(spack.modules, 'module_types', {factory.name: factory})
    return factory


@pytest.fixture()
def lmod_factory(tmpdir, monkeypatch):
    """Returns a factory that writes hierarchical LUA module files."""
    factory = spack.modules.LmodModule
    monkeypatch.setattr(factory, 'path', str(tmpdir))
    monkeypatch.setattr(spack.modules, 'module_types', {factory.name: factory})
    return factory


@pytest.fixture()
def dotkit_factory(tmpdir, monkeypatch):
    """Returns a factory that writes DotKit module files."""
    factory = spack.modules.Dotkit
    monkeypatch.setattr(factory, 'path', str(tmpdir))
    monkeypatch.setattr(spack.modules, 'module_types', {factory.name: factory})
    return factory


@pytest.mark.usefixtures('config', 'builtin_mock', 'stringio_open')
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

    def test_simple_case(self, tcl_factory):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpich_spec_string)
        content = get_modulefile_content(tcl_factory, spec)
        assert 'module-whatis "mpich @3.0.4"' in content
        with pytest.raises(TypeError):
            spack.modules.dependencies(spec, 'non-existing-tag')

    def test_autoload(self, tcl_factory):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 5
        assert len([x for x in content if 'module load ' in x]) == 5

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec('dtbuild1')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec('dtbuild1')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

    def test_prerequisites(self, tcl_factory):
        spack.modules._module_config = self.configuration_prerequisites_direct
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'prereq' in x]) == 2

        spack.modules._module_config = self.configuration_prerequisites_all
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'prereq' in x]) == 5

    def test_alter_environment(self, tcl_factory):
        spack.modules._module_config = self.configuration_alter_environment
        spec = spack.spec.Spec('mpileaks platform=test target=x86_64')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 1
        assert len([x for x in content if 'unsetenv BAR' in x]) == 1
        assert len([x for x in content if 'setenv MPILEAKS_ROOT' in x]) == 1

        spec = spack.spec.Spec('libdwarf %clang platform=test target=x86_32')
        content = get_modulefile_content(tcl_factory, spec)
        assert len(
            [x for x in content if x.startswith('prepend-path CMAKE_PREFIX_PATH')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 0
        assert len([x for x in content if 'is-loaded foo/bar' in x]) == 1
        assert len([x for x in content if 'module load foo/bar' in x]) == 1
        assert len([x for x in content if 'setenv LIBDWARF_ROOT' in x]) == 1

    def test_blacklist(self, tcl_factory):
        spack.modules._module_config = self.configuration_blacklist
        spec = spack.spec.Spec('mpileaks ^zmpi')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1
        spec = spack.spec.Spec('callpath arch=x86-linux')
        # Returns a StringIO instead of a string as no module file was written
        with pytest.raises(AttributeError):
            get_modulefile_content(tcl_factory, spec)
        spec = spack.spec.Spec('zmpi arch=x86-linux')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

    def test_conflicts(self, tcl_factory):
        spack.modules._module_config = self.configuration_conflicts
        spec = spack.spec.Spec('mpileaks')
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if x.startswith('conflict')]) == 2
        assert len([x for x in content if x == 'conflict mpileaks']) == 1
        assert len([x for x in content if x == 'conflict intel/14.0.1']) == 1

        spack.modules._module_config = self.configuration_wrong_conflicts
        with pytest.raises(SystemExit):
            get_modulefile_content(tcl_factory, spec)

    def test_suffixes(self, tcl_factory):
        spack.modules._module_config = self.configuration_suffix
        spec = spack.spec.Spec('mpileaks+debug arch=x86-linux')
        spec.concretize()
        generator = tcl_factory(spec)
        assert 'foo' in generator.use_name

        spec = spack.spec.Spec('mpileaks~debug arch=x86-linux')
        spec.concretize()
        generator = tcl_factory(spec)
        assert 'bar' in generator.use_name

    def test_setup_environment(self, tcl_factory):
        spec = spack.spec.Spec('mpileaks')
        spec.concretize()
        content = get_modulefile_content(tcl_factory, spec)
        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "mpileaks"' in x]
        ) == 1

        content = get_modulefile_content(tcl_factory, spec['callpath'])
        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "callpath"' in x]
        ) == 1


@pytest.mark.usefixtures('config', 'builtin_mock', 'stringio_open')
class TestLmod(object):
    configuration_autoload_direct = {
        'enable': ['lmod'],
        'lmod': {
            'all': {
                'autoload': 'direct'
            }
        }
    }

    configuration_autoload_all = {
        'enable': ['lmod'],
        'lmod': {
            'all': {
                'autoload': 'all'
            }
        }
    }

    configuration_no_hash = {
        'enable': ['lmod'],
        'lmod': {
            'hash_length': 0
        }
    }

    configuration_alter_environment = {
        'enable': ['lmod'],
        'lmod': {
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
            'blacklist': ['callpath'],
            'all': {
                'autoload': 'direct'
            }
        }
    }

    def test_simple_case(self, lmod_factory):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpich_spec_string)
        content = get_modulefile_content(lmod_factory, spec)
        assert '-- -*- lua -*-' in content
        assert 'whatis([[Name : mpich]])' in content
        assert 'whatis([[Version : 3.0.4]])' in content

    def test_autoload(self, lmod_factory):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = get_modulefile_content(lmod_factory, spec)
        assert len([x for x in content if 'if not isloaded(' in x]) == 2
        assert len([x for x in content if 'load(' in x]) == 2

        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = get_modulefile_content(lmod_factory, spec)
        assert len([x for x in content if 'if not isloaded(' in x]) == 5
        assert len([x for x in content if 'load(' in x]) == 5

    def test_alter_environment(self, lmod_factory):
        spack.modules._module_config = self.configuration_alter_environment
        spec = spack.spec.Spec('mpileaks platform=test target=x86_64')
        content = get_modulefile_content(lmod_factory, spec)
        assert len(
            [x for x in content if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 1
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 1

        spec = spack.spec.Spec('libdwarf %clang platform=test target=x86_32')
        content = get_modulefile_content(lmod_factory, spec)
        assert len(
            [x for x in content if x.startswith('prepend-path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 0
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 0

    def test_blacklist(self, lmod_factory):
        spack.modules._module_config = self.configuration_blacklist
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = get_modulefile_content(lmod_factory, spec)
        assert len([x for x in content if 'if not isloaded(' in x]) == 1
        assert len([x for x in content if 'load(' in x]) == 1

    def test_no_hash(self, lmod_factory):
        # Make sure that virtual providers (in the hierarchy) always
        # include a hash. Make sure that the module file for the spec
        # does not include a hash if hash_length is 0.
        spack.modules._module_config = self.configuration_no_hash
        spec = spack.spec.Spec(mpileaks_spec_string)
        spec.concretize()
        module = lmod_factory(spec)
        path = module.file_name
        mpi_spec = spec['mpi']
        mpiElement = "{0}/{1}-{2}/".format(
            mpi_spec.name, mpi_spec.version, mpi_spec.dag_hash(length=7)
        )
        assert mpiElement in path
        mpileaks_spec = spec
        mpileaks_element = "{0}/{1}.lua".format(
            mpileaks_spec.name, mpileaks_spec.version)
        assert path.endswith(mpileaks_element)


@pytest.mark.usefixtures('config', 'builtin_mock', 'stringio_open')
class TestDotkit(object):
    configuration_dotkit = {
        'enable': ['dotkit'],
        'dotkit': {
            'all': {
                'prerequisites': 'direct'
            }
        }
    }

    def test_dotkit(self, dotkit_factory):
        spack.modules._module_config = self.configuration_dotkit
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = get_modulefile_content(dotkit_factory, spec)
        assert '#c spack' in content
        assert '#d mpileaks @2.3' in content
