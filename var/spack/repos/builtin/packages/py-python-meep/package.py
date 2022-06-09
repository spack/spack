# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonMeep(PythonPackage):
    """Python-meep is a wrapper around libmeep. It allows the scripting of
    Meep-simulations with Python"""

    homepage = "https://launchpad.net/python-meep"
    url      = "https://launchpad.net/python-meep/1.4/1.4/+download/python-meep-1.4.2.tar"

    version('1.4.2', sha256='d91428aa4727c308383cea31ca9cdacee409320c686e9a8368769933e56c8762')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('python@2.6:2.7', type=('build', 'run'))
    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    depends_on('mpi', when='+mpi')
    depends_on('meep~mpi', when='~mpi')
    depends_on('meep+mpi', when='+mpi')

    # As of SWIG 3.0.3, Python-style comments are now treated as
    # pre-processor directives. Use older SWIG. But not too old,
    # or else it can't handle newer C++ compilers and flags.
    depends_on('swig@1.3.39:3.0.2')

    def patch(self):
        if '+mpi' in self.spec:
            copy('setup-mpi.py', 'setup.py')
