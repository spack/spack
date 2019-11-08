# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack import *


class Timemory(CMakePackage):
    """Timing + Memory + Hardware Counter Utilities for C/C++/CUDA/Python"""

    homepage = 'https://timemory.readthedocs.io/en/latest/'
    git = 'https://github.com/NERSC/timemory.git'
    maintainers = ['jrmadsen']

    version('master', branch='master', submodules=True)

    variant('python', default=True, description='Enable Python support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('papi', default=True, description='Enable PAPI support')
    variant('cuda', default=True, description='Enable CUDA support')
    variant('cupti', default=True, description='Enable CUPTI support')
    variant('caliper', default=True, description='Enable Caliper support')
    variant('gperftools', default=True, description='Enable gperftools support')

    depends_on('cmake@3.10:', type='build')

    extends('python', when='+python')
    depends_on('python@3:', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('run'))
    depends_on('py-pillow', when='+python', type=('run'))
    depends_on('py-matplotlib', when='+python', type=('run'))
    depends_on('mpi', when='+mpi')
    depends_on('papi', when='+papi')
    depends_on('cuda', when='+cuda')
    depends_on('caliper', when='+caliper')
    depends_on('gperftools', when='+gperftools')

    def cmake_args(self):
        spec = self.spec

        # Use spack install of Caliper instead of internal build
        args = [
            '-DTIMEMORY_BUILD_CALIPER=OFF',
            '-DTIMEMORY_BUILD_TOOLS=ON',
            '-DTIMEMORY_BUILD_EXTRA_OPTIMIZATIONS=ON',
            '-DTIMEMORY_BUILD_GTEST=OFF',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON',
        ]

        if '+python' in spec:
            args.append('-DPYTHON_EXECUTABLE={0}'.format(
                spec['python'].command.path))
            args.append('-DTIMEMORY_BUILD_PYTHON=ON')
            args.append('-DTIMEMORY_TLS_MODEL=global-dynamic')
        else:
            args.append('-DTIMEMORY_BUILD_PYTHON=OFF')

        if '+caliper' in spec:
            args.append('-DTIMEMORY_USE_CALIPER=ON')
        else:
            args.append('-DTIMEMORY_USE_CALIPER=OFF')

        if '+papi' in spec:
            args.append('-DTIMEMORY_USE_PAPI=ON')
            args.append('-DPAPI_ROOT_DIR={0}'.format(spec['papi'].prefix))
        else:
            args.append('-DTIMEMORY_USE_PAPI=OFF')

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DMPI_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
        else:
            args.append('-DTIMEMORY_USE_MPI=OFF')

        if '+cupti' in spec:
            args.append('-DTIMEMORY_USE_CUPTI=ON')
        else:
            args.append('-DTIMEMORY_USE_CUPTI=OFF')

        return args
