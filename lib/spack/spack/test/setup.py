import re
import os
import contextlib
import imp
import tempfile
import unittest
import shutil

import pytest
import spack
import spack.stage
import spack.util.executable


@contextlib.contextmanager
def prepend_path(path):
    old_path = sys.path
    sys.path = [path] + sys.path
    yield
    sys.path = old_path


@pytest.mark.usefixtures('builtin_mock')
class TestSetup(unittest.TestCase):

    def setUp(self):
        self.orig_environ = os.environ
        os.environ = os.environ.copy()

        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        os.environ = self.orig_environ
        shutil.rmtree(self.dir)

    def test_setup_cmake(self):
        """Generate an spconfig.py file from CMake and verify key parts of
        it."""

        # Spec from cli
        spec = spack.cmd.parse_specs(
            'everytrace', concretize=True, allow_multi=False)

        fname = os.path.join(self.dir, 'spconfig.py')

        spack.build_environment.setup_package(spec.package)
        os.environ['SPACK_CC'] = '/dummy/cc'
        os.environ['SPACK_CXX'] = '/dummy/cxx'
        try:
            del os.environ['SPACK_FC']
        except:
            pass

        # Write spconfig.py; then import it into Python for inspection
        with open(fname, 'w') as fout:
            spec.package._write_spconfig(fout)
        spconfig = imp.load_source('spconfig', fname)

        env = spconfig.env
        self.assertEqual('/dummy/cc', env['CC'])
        self.assertEqual('/dummy/cxx', env['CXX'])
        self.assertFalse('FC' in env)
        self.assertEqual(
            env['SPACK_TRANSITIVE_INCLUDE_PATH'],
            os.path.join(env['CMAKE_PREFIX_PATH'], 'include'))

        defs = dict()
        defre = re.compile('-D(.*?)(:(.*?))?=(.*)')
        print(spconfig.cmd)
        for arg in spconfig.cmd:
            match = defre.match(arg)
            if match is None:
                continue
            defs[match.group(1)] = match.group(4)

        self.assertEqual(spec.prefix, defs['CMAKE_INSTALL_PREFIX'])
        self.assertEqual('RelWithDebInfo', defs['CMAKE_BUILD_TYPE'])
        self.assertEqual('FALSE', defs['CMAKE_INSTALL_RPATH_USE_LINK_PATH'])
        self.assertEqual('NO', defs['USE_MPI'])
        self.assertEqual('NO', defs['USE_FORTRAN'])
