# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
from spack import *


class Parsec(CMakePackage, CudaPackage):
    """PaRSEC: the Parallel Runtime Scheduler and Execution Controller

    PaRSEC is a runtime and a programming toolbox that support the design and
    parallel execution of micro-tasks on distributed, heterogeneous systems.
    """

    homepage    = "https://icl.utk.edu/dte"
    git         = "https://bitbucket.org/icldistcomp/parsec.git"
    url         = "https://bitbucket.org/icldistcomp/parsec/get/parsec-3.0.2012.tar.bz2"
    list_url    = "https://bitbucket.org/icldistcomp/parsec/downloads/?tab=tags"
    maintainers = ['abouteiller', 'bosilca', 'herault']

    version('master', branch='master')
    version('3.0.2012-rc1', sha256='a0f013bd5a2c44c61d3d76bab102e3ca3bab68ef2e89d7b5f544b9c1a6fde475')
    version('1.1.0', sha256='d2928033c121000ae0a554f1e7f757c1f22274a8b74457ecd52744ae1f70b95a', url='https://bitbucket.org/icldistcomp/parsec/get/v1.1.0.tar.bz2')

    variant('build_type', default='RelWithDebInfo', description='CMake build type', values=('Debug', 'Release', 'RelWithDebInfo'))
    variant('shared', default=True, description='Build a shared library')
    variant('cuda', default=True, description='Build with CUDA')
    variant('profile', default=False, description='Generate profiling data')
    variant('debug_verbose', default=False, description='Debug version with verbose and paranoid (incurs performance overhead!)')
    conflicts('+debug_verbose build_type=Release', msg='You need to set build_type=Debug for +debug_verbose')
    conflicts('+debug_verbose build_type=RelWithDebInfo', msg='You need to set build_type=Debug for +debug_verbose')
    # TODO: Spack does not handle cross-compilation atm
    # variant('xcompile', default=False, description='Cross compile')

    depends_on('cmake@3.16.0:', type='build')
    depends_on('python', type='build')
    depends_on('hwloc')
    depends_on('mpi')
    depends_on('papi', when='+profile')
    depends_on('python', type=('build', 'run'), when='+profile')
    depends_on('py-cython', type=('build', 'run'), when='+profile')
    depends_on('py-pandas', type=('build', 'run'), when='+profile')
    depends_on('py-matplotlib', type=('build', 'run'),  when='+profile')
    depends_on('py-tables', type=('build', 'run'), when='+profile')

    def cmake_args(self):
        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('PARSEC_GPU_WITH_CUDA', 'cuda'),
            self.define_from_variant('PARSEC_PROF_TRACE', 'profile'),
            self.define_from_variant('PARSEC_DEBUG_HISTORY', 'debug_verbose'),
            self.define_from_variant('PARSEC_DEBUG_PARANOID', 'debug_verbose'),
        ]
        return args
