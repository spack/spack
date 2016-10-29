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
from contextlib import contextmanager

import StringIO
import spack.modules
import spack.spec
import llnl.util.filesystem
from spack.test.mock_packages_test import MockPackagesTest

FILE_REGISTRY = collections.defaultdict(StringIO.StringIO)


# Monkey-patch open to write module files to a StringIO instance
@contextmanager
def mock_open(filename, mode):
    if not mode == 'w':
        raise RuntimeError(
            'test.modules : unexpected opening mode for monkey-patched open')

    FILE_REGISTRY[filename] = StringIO.StringIO()

    try:
        yield FILE_REGISTRY[filename]
    finally:
        handle = FILE_REGISTRY[filename]
        FILE_REGISTRY[filename] = handle.getvalue()
        handle.close()


# Spec strings that will be used throughout the tests
mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf arch=x64-linux'


class HelperFunctionsTests(MockPackagesTest):

    def test_update_dictionary_extending_list(self):
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
        self.assertTrue(len(target) == 4)
        self.assertTrue(len(target['foo']) == 4)
        self.assertTrue(len(target['bar']) == 4)
        self.assertEqual(target['baz'], 'foobaz')

    def test_inspect_path(self):
        env = spack.modules.inspect_path('/usr')
        names = [item.name for item in env]
        self.assertTrue('PATH' in names)
        self.assertTrue('LIBRARY_PATH' in names)
        self.assertTrue('LD_LIBRARY_PATH' in names)
        self.assertTrue('CPATH' in names)


class ModuleFileGeneratorTests(MockPackagesTest):
    """
    Base class to test module file generators. Relies on child having defined
    a 'factory' attribute to create an instance of the generator to be tested.
    """

    def setUp(self):
        super(ModuleFileGeneratorTests, self).setUp()
        self.configuration_instance = spack.modules._module_config
        self.module_types_instance = spack.modules.module_types
        spack.modules.open = mock_open
        spack.modules.mkdirp = lambda x: None
        # Make sure that a non-mocked configuration will trigger an error
        spack.modules._module_config = None
        spack.modules.module_types = {self.factory.name: self.factory}

    def tearDown(self):
        del spack.modules.open
        spack.modules.module_types = self.module_types_instance
        spack.modules._module_config = self.configuration_instance
        spack.modules.mkdirp = llnl.util.filesystem.mkdirp
        super(ModuleFileGeneratorTests, self).tearDown()

    def get_modulefile_content(self, spec):
        spec.concretize()
        generator = self.factory(spec)
        generator.write()
        content = FILE_REGISTRY[generator.file_name].split('\n')
        generator.remove()
        return content


class TclTests(ModuleFileGeneratorTests):

    factory = spack.modules.TclModule

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

    def test_simple_case(self):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpich_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertTrue('module-whatis "mpich @3.0.4"' in content)
        self.assertRaises(TypeError, spack.modules.dependencies,
                          spec, 'non-existing-tag')

    def test_autoload(self):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 2)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 2)

        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 5)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 5)

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec('dtbuild1')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 2)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 2)

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec('dtbuild1')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 2)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 2)

    def test_prerequisites(self):
        spack.modules._module_config = self.configuration_prerequisites_direct
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'prereq' in x]), 2)

        spack.modules._module_config = self.configuration_prerequisites_all
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'prereq' in x]), 5)

    def test_alter_environment(self):
        spack.modules._module_config = self.configuration_alter_environment
        spec = spack.spec.Spec('mpileaks platform=test target=x86_64')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend-path CMAKE_PREFIX_PATH')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv FOO "foo"' in x]), 1)
        self.assertEqual(len([x for x in content if 'unsetenv BAR' in x]), 1)
        self.assertEqual(
            len([x for x in content if 'setenv MPILEAKS_ROOT' in x]), 1)

        spec = spack.spec.Spec('libdwarf %clang platform=test target=x86_32')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend-path CMAKE_PREFIX_PATH')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv FOO "foo"' in x]), 0)
        self.assertEqual(len([x for x in content if 'unsetenv BAR' in x]), 0)
        self.assertEqual(
            len([x for x in content if 'is-loaded foo/bar' in x]), 1)
        self.assertEqual(
            len([x for x in content if 'module load foo/bar' in x]), 1)
        self.assertEqual(
            len([x for x in content if 'setenv LIBDWARF_ROOT' in x]), 1)

    def test_blacklist(self):
        spack.modules._module_config = self.configuration_blacklist
        spec = spack.spec.Spec('mpileaks ^zmpi')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 1)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 1)
        spec = spack.spec.Spec('callpath arch=x86-linux')
        # Returns a StringIO instead of a string as no module file was written
        self.assertRaises(AttributeError, self.get_modulefile_content, spec)
        spec = spack.spec.Spec('zmpi arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 1)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 1)

    def test_conflicts(self):
        spack.modules._module_config = self.configuration_conflicts
        spec = spack.spec.Spec('mpileaks')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x for x in content if x.startswith('conflict')]), 2)
        self.assertEqual(
            len([x for x in content if x == 'conflict mpileaks']), 1)
        self.assertEqual(
            len([x for x in content if x == 'conflict intel/14.0.1']), 1)

        spack.modules._module_config = self.configuration_wrong_conflicts
        self.assertRaises(SystemExit, self.get_modulefile_content, spec)

    def test_suffixes(self):
        spack.modules._module_config = self.configuration_suffix
        spec = spack.spec.Spec('mpileaks+debug arch=x86-linux')
        spec.concretize()
        generator = spack.modules.TclModule(spec)
        self.assertTrue('foo' in generator.use_name)

        spec = spack.spec.Spec('mpileaks~debug arch=x86-linux')
        spec.concretize()
        generator = spack.modules.TclModule(spec)
        self.assertTrue('bar' in generator.use_name)


class LmodTests(ModuleFileGeneratorTests):
    factory = spack.modules.LmodModule

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

    def test_simple_case(self):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpich_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertTrue('-- -*- lua -*-' in content)
        self.assertTrue('whatis([[Name : mpich]])' in content)
        self.assertTrue('whatis([[Version : 3.0.4]])' in content)

    def test_autoload(self):
        spack.modules._module_config = self.configuration_autoload_direct
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x for x in content if 'if not isloaded(' in x]), 2)
        self.assertEqual(len([x for x in content if 'load(' in x]), 2)

        spack.modules._module_config = self.configuration_autoload_all
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x for x in content if 'if not isloaded(' in x]), 5)
        self.assertEqual(len([x for x in content if 'load(' in x]), 5)

    def test_alter_environment(self):
        spack.modules._module_config = self.configuration_alter_environment
        spec = spack.spec.Spec('mpileaks platform=test target=x86_64')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv("FOO", "foo")' in x]), 1)
        self.assertEqual(
            len([x for x in content if 'unsetenv("BAR")' in x]), 1)

        spec = spack.spec.Spec('libdwarf %clang platform=test target=x86_32')
        content = self.get_modulefile_content(spec)
        print('\n'.join(content))
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend-path("CMAKE_PREFIX_PATH"')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv("FOO", "foo")' in x]), 0)
        self.assertEqual(
            len([x for x in content if 'unsetenv("BAR")' in x]), 0)

    def test_blacklist(self):
        spack.modules._module_config = self.configuration_blacklist
        spec = spack.spec.Spec(mpileaks_spec_string)
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x for x in content if 'if not isloaded(' in x]), 1)
        self.assertEqual(len([x for x in content if 'load(' in x]), 1)

    def test_no_hash(self):
        # Make sure that virtual providers (in the hierarchy) always
        # include a hash. Make sure that the module file for the spec
        # does not include a hash if hash_length is 0.
        spack.modules._module_config = self.configuration_no_hash
        spec = spack.spec.Spec(mpileaks_spec_string)
        spec.concretize()
        module = spack.modules.LmodModule(spec)
        path = module.file_name
        mpiSpec = spec['mpi']
        mpiElement = "{0}/{1}-{2}/".format(
            mpiSpec.name, mpiSpec.version, mpiSpec.dag_hash(length=7))
        self.assertTrue(mpiElement in path)
        mpileaksSpec = spec
        mpileaksElement = "{0}/{1}.lua".format(
            mpileaksSpec.name, mpileaksSpec.version)
        self.assertTrue(path.endswith(mpileaksElement))


class DotkitTests(MockPackagesTest):

    configuration_dotkit = {
        'enable': ['dotkit'],
        'dotkit': {
            'all': {
                'prerequisites': 'direct'
            }
        }
    }

    def setUp(self):
        super(DotkitTests, self).setUp()
        self.configuration_obj = spack.modules._module_config
        spack.modules.open = mock_open
        # Make sure that a non-mocked configuration will trigger an error
        spack.modules._module_config = None

    def tearDown(self):
        del spack.modules.open
        spack.modules._module_config = self.configuration_obj
        super(DotkitTests, self).tearDown()

    def get_modulefile_content(self, spec):
        spec.concretize()
        generator = spack.modules.Dotkit(spec)
        generator.write()
        content = FILE_REGISTRY[generator.file_name].split('\n')
        return content

    def test_dotkit(self):
        spack.modules._module_config = self.configuration_dotkit
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertTrue('#c spack' in content)
        self.assertTrue('#d mpileaks @2.3' in content)
