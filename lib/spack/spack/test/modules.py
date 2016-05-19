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

configuration_alter_environment = {
    'enable': ['tcl'],
    'tcl': {
        'all': {
            'filter': {'environment_blacklist': ['CMAKE_PREFIX_PATH']}
        },
        'arch=x86-linux': {
            'environment': {'set': {'FOO': 'foo'},
                            'unset': ['BAR']}
        }
    }
}

configuration_blacklist = {
    'enable': ['tcl'],
    'tcl': {
        'blacklist': ['callpath'],
        'all': {
            'autoload': 'direct'
        }
    }
}

configuration_conflicts = {
    'enable': ['tcl'],
    'tcl': {
        'naming_scheme': '{name}/{version}-{compiler.name}',
        'all': {
            'conflict': ['{name}', 'intel/14.0.1']
        }
    }
}


class TclTests(MockPackagesTest):
    def setUp(self):
        super(TclTests, self).setUp()
        self.configuration_obj = spack.modules.CONFIGURATION
        spack.modules.open = mock_open
        # Make sure that a non-mocked configuration will trigger an error
        spack.modules.CONFIGURATION = None

    def tearDown(self):
        del spack.modules.open
        spack.modules.CONFIGURATION = self.configuration_obj
        super(TclTests, self).tearDown()

    def get_modulefile_content(self, spec):
        spec.concretize()
        generator = spack.modules.TclModule(spec)
        generator.write()
        content = FILE_REGISTRY[generator.file_name].split('\n')
        return content

    def test_simple_case(self):
        spack.modules.CONFIGURATION = configuration_autoload_direct
        spec = spack.spec.Spec('mpich@3.0.4 arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertTrue('module-whatis "mpich @3.0.4"' in content)

    def test_autoload(self):
        spack.modules.CONFIGURATION = configuration_autoload_direct
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 2)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 2)

        spack.modules.CONFIGURATION = configuration_autoload_all
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 5)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 5)

    def test_alter_environment(self):
        spack.modules.CONFIGURATION = configuration_alter_environment
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend-path CMAKE_PREFIX_PATH')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv FOO "foo"' in x]), 1)
        self.assertEqual(len([x for x in content if 'unsetenv BAR' in x]), 1)

        spec = spack.spec.Spec('libdwarf arch=x64-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x
                 for x in content
                 if x.startswith('prepend-path CMAKE_PREFIX_PATH')]), 0)
        self.assertEqual(
            len([x for x in content if 'setenv FOO "foo"' in x]), 0)
        self.assertEqual(len([x for x in content if 'unsetenv BAR' in x]), 0)

    def test_blacklist(self):
        spack.modules.CONFIGURATION = configuration_blacklist
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(len([x for x in content if 'is-loaded' in x]), 1)
        self.assertEqual(len([x for x in content if 'module load ' in x]), 1)

    def test_conflicts(self):
        spack.modules.CONFIGURATION = configuration_conflicts
        spec = spack.spec.Spec('mpileaks arch=x86-linux')
        content = self.get_modulefile_content(spec)
        self.assertEqual(
            len([x for x in content if x.startswith('conflict')]), 2)
        self.assertEqual(
            len([x for x in content if x == 'conflict mpileaks']), 1)
        self.assertEqual(
            len([x for x in content if x == 'conflict intel/14.0.1']), 1)
