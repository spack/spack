# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OmegaH(CMakePackage):
    """Omega_h is a C++11 library providing data structures and algorithms
    for adaptive discretizations. Its specialty is anisotropic triangle and
    tetrahedral mesh adaptation. It runs efficiently on most modern HPC
    hardware including GPUs.
    """

    homepage = "https://github.com/SNLComputation/omega_h"
    url      = "https://github.com/SNLComputation/omega_h/archive/v9.22.1.tar.gz"
    git      = "https://github.com/SNLComputation/omega_h.git"

    version('develop', branch='master')
    version('9.22.2', sha256='ab5636be9dc171a514a7015df472bd85ab86fa257806b41696170842eabea37d')
    version('9.22.1', sha256='e45907210b7992aa6168e8e8435482d032c2a504b0c0fe222715ce67e7998bf4')
    version('9.21.1', sha256='750415614747681c0094d3103e7683c74edcd95819ef9477f2179c805c416cfa')
    version('9.20.2', sha256='e1491969ccb170a92018a8b7d02f34b6177deffcbba74bc7c2ee862793a846c8')
    version('9.19.1', sha256='60ef65c2957ce03ef9d1b995d842fb65c32c5659d064de002c071effe66b1b1f')
    version('9.18.1', sha256='333c93e28c56173afd2815274fa2bde25d361edc4a8a9a28f90c3a3e144512c3')

    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('zlib', default=True, description='Activates ZLib support')
    variant('trilinos', default=False, description='Use Teuchos and Kokkos')
    variant('build_type', default='')
    variant('throw', default=False, description='Errors throw exceptions instead of abort')
    variant('examples', default=False, description='Compile examples')
    variant('optimize', default=True, description='Compile C++ with optimization')
    variant('symbols', default=True, description='Compile C++ with debug symbols')
    variant('warnings', default=False, description='Compile C++ with warnings')

    depends_on('gmsh', when='+examples', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos +kokkos +teuchos', when='+trilinos')
    depends_on('zlib', when='+zlib')

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86610
    conflicts('%gcc@8:')

    def _bob_options(self):
        cmake_var_prefix = 'Omega_h_CXX_'
        for variant in ['optimize', 'symbols', 'warnings']:
            cmake_var = cmake_var_prefix + variant.upper()
            if '+' + variant in self.spec:
                yield '-D' + cmake_var + ':BOOL=ON'
            else:
                yield '-D' + cmake_var + ':BOOL=FALSE'

    def cmake_args(self):
        args = ['-DUSE_XSDK_DEFAULTS:BOOL=OFF']
        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        if '+mpi' in self.spec:
            args.append('-DOmega_h_USE_MPI:BOOL=ON')
            args.append('-DCMAKE_CXX_COMPILER:FILEPATH={0}'.format(
                self.spec['mpi'].mpicxx))
        else:
            args.append('-DOmega_h_USE_MPI:BOOL=OFF')
        if '+trilinos' in self.spec:
            args.append('-DOmega_h_USE_Trilinos:BOOL=ON')
        if '+zlib' in self.spec:
            args.append('-DOmega_h_USE_ZLIB:BOOL=ON')
            args.append('-DZLIB_ROOT:PATH={0}'.format(
                self.spec['zlib'].prefix))
        else:
            args.append('-DOmega_h_USE_ZLIB:BOOL=OFF')
        if '+examples' in self.spec:
            args.append('-DOmega_h_EXAMPLES:BOOL=ON')
        else:
            args.append('-DOmega_h_EXAMPLES:BOOL=OFF')
        if '+throw' in self.spec:
            args.append('-DOmega_h_THROW:BOOL=ON')
        else:
            args.append('-DOmega_h_THROW:BOOL=OFF')
        args += list(self._bob_options())
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
