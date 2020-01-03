# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    version('develop', branch='develop', submodules=True)
    version('3.0.1', commit='ef638e1cde90275ce7c0e12fc4902c27bcbdeefd',
            submodules=True)
    version('3.0.0', commit='b36b1673b2c6b7ff3126d8261bef0f8f176c7beb',
            submodules=True)

    variant('python', default=True, description='Enable Python support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('tau', default=True, description='Enable TAU support')
    variant('papi', default=True, description='Enable PAPI support')
    variant('cuda', default=True, description='Enable CUDA support')
    variant('cupti', default=True, description='Enable CUPTI support')
    variant('upcxx', default=False, description='Enable UPC++ support')
    variant('gotcha', default=True, description='Enable GOTCHA support')
    variant('likwid', default=True, description='Enable LIKWID support')
    variant('caliper', default=True, description='Enable Caliper support')
    variant('gperftools', default=True,
            description='Enable gperftools support')

    depends_on('cmake@3.11:', type='build')

    extends('python', when='+python')
    depends_on('python@3:', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('run'))
    depends_on('py-pillow', when='+python', type=('run'))
    depends_on('py-matplotlib', when='+python', type=('run'))
    depends_on('mpi', when='+mpi')
    depends_on('tau', when='+tau')
    depends_on('papi', when='+papi')
    depends_on('cuda', when='+cuda')
    depends_on('cuda', when='+cupti')
    depends_on('upcxx', when='+upcxx')
    depends_on('gotcha', when='+gotcha')
    depends_on('likwid', when='+likwid')
    depends_on('caliper', when='+caliper')
    depends_on('gperftools', when='+gperftools')

    conflicts('+cupti', when='~cuda', msg='CUPTI requires CUDA')

    def cmake_args(self):
        spec = self.spec

        # Use spack install of Caliper and/or GOTCHA
        # instead of internal submodule build
        args = [
            '-DTIMEMORY_BUILD_GOTCHA=OFF',
            '-DTIMEMORY_BUILD_CALIPER=OFF',
            '-DTIMEMORY_BUILD_TOOLS=ON',
            '-DTIMEMORY_BUILD_TESTING=OFF',
            '-DTIMEMORY_BUILD_EXTRA_OPTIMIZATIONS=ON',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON',
        ]

        if '+python' in spec:
            args.append('-DPYTHON_EXECUTABLE={0}'.format(
                spec['python'].command.path))
            args.append('-DTIMEMORY_USE_PYTHON=ON')
            args.append('-DTIMEMORY_BUILD_PYTHON=ON')
            args.append('-DTIMEMORY_TLS_MODEL=global-dynamic')
        else:
            args.append('-DTIMEMORY_USE_PYTHON=OFF')
            args.append('-DTIMEMORY_BUILD_PYTHON=OFF')

        if '+caliper' in spec:
            args.append('-DTIMEMORY_USE_CALIPER=ON')
        else:
            args.append('-DTIMEMORY_USE_CALIPER=OFF')

        if '+tau' in spec:
            args.append('-DTIMEMORY_USE_TAU=ON')
        else:
            args.append('-DTIMEMORY_USE_TAU=OFF')

        if '+likwid' in spec:
            args.append('-DTIMEMORY_USE_LIKWID=ON')
        else:
            args.append('-DTIMEMORY_USE_LIKWID=OFF')

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

        if '+gotcha' in spec:
            args.append('-DTIMEMORY_USE_GOTCHA=ON')
        else:
            args.append('-DTIMEMORY_USE_GOTCHA=OFF')

        if '+cuda' in spec:
            args.append('-DTIMEMORY_USE_CUDA=ON')
        else:
            args.append('-DTIMEMORY_USE_CUDA=OFF')

        if '+cupti' in spec:
            args.append('-DTIMEMORY_USE_CUPTI=ON')
        else:
            args.append('-DTIMEMORY_USE_CUPTI=OFF')

        return args
