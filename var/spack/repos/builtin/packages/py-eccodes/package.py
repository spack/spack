# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package_defs import *


class PyEccodes(PythonPackage):
    """Python interface to the ecCodes GRIB and BUFR decoder/encoder."""

    homepage = "https://github.com/ecmwf/eccodes-python"
    pypi     = "eccodes/eccodes-1.3.2.tar.gz"

    version('1.3.2', sha256='f282adfdc1bc658356163c9cef1857d4b2bae99399660d3d4fcb145a52d3b2a6')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('py-findlibs', type=('build', 'run'))
    depends_on('eccodes', type='run')

    def setup_build_environment(self, env):
        if sys.platform == 'darwin':
            env.prepend_path('DYLD_LIBRARY_PATH',
                             self.spec['eccodes'].libs.directories[0])
        else:
            env.prepend_path('LD_LIBRARY_PATH',
                             self.spec['eccodes'].libs.directories[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def test(self):
        super(PyEccodes, self).test()

        self.run_test(self.spec['python'].command.path,
                      ['-m', 'eccodes', 'selfcheck'],
                      purpose='checking system setup',
                      work_dir='spack-test')
