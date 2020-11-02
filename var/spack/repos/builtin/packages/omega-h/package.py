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
    url      = "https://github.com/BlueBrain/omega_h/archive/v9.22.1.tar.gz"
    git      = "https://github.com/BlueBrain/omega_h.git"

    version('develop', branch='master')
    version('9.32.5.dev3', sha256='83381f728688ad9d786f02946fe101bf577c7c3268a40e46264935e7cd1a5d97')
    version('9.31.3.dev2', sha256='8ff448a5185e916068dc41e25a0e7a262d12543426c3888ae145ed90a7afa0de')
    version('9.31.2.dev2', sha256='08be63b68a012ed8fcf4b7a217cbaadf46faa3f3c937ec8224ff9c542eb6ae62')
    version('9.31.2', sha256='df859bc8ae0e4bcd9c4f6654b6951c7e34110ac3b3e7d2b0c1e413ce2645772d')
    version('9.30.0', sha256='7160045ea12718269f345c7be93a386533ebb76788504df413f22fbcb072f158')
    version('9.29.2', sha256='8eea6da0ebde44176a6d19fb858f89f872611cbad08cad65700757e096058465')
    version('9.29.0', sha256='b41964b018909ffe9cea91c23a0509b259bfbcf56874fcdf6bd9f6a179938014')
    version('9.28.0', sha256='681588974116025c6c1c535972386c23fe354502319fcbbbdc5b9d373429c08e')
    version('9.27.3', sha256='7c0b0c9c00cda97763be1287d3bf8b931bcdd07bf4971fc7258a3892d628cf20')
    version('9.27.0', sha256='aa51f83508cbd14a41ae953bda7da98a6ad2979465c76e5b3a3d9a7a651cb34a')
    version('9.26.6', sha256='5022bf3f9be1a27668fd2ec396d66f6b0124dc4a3adeedb20a580a701d37d893')
    version('9.25.4', sha256='9a9b26d5c4fc352776c1da02d787e653b5878c0cca3890eefebd3df202c75aed')
    version('9.24.2', sha256='af084e56204262c2a7edcc9c88e997623fc1280ae59427b9bf2b57d11568b496')
    version('9.22.2', sha256='ab5636be9dc171a514a7015df472bd85ab86fa257806b41696170842eabea37d')
    version('9.21.1', sha256='750415614747681c0094d3103e7683c74edcd95819ef9477f2179c805c416cfa')

    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('zlib', default=True, description='Activates ZLib support')
    variant('trilinos', default=False, description='Use Teuchos and Kokkos')
    variant('build_type', default='RelWithDebugInfo')
    variant('throw', default=False, description='Errors throw exceptions instead of abort')
    variant('examples', default=False, description='Compile examples')
    variant('optimize', default=True, description='Compile C++ with optimization')
    variant('symbols', default=True, description='Compile C++ with debug symbols')
    variant('warnings', default=False, description='Compile C++ with warnings')
    variant('gmsh', default=False, description='Use Gmsh C++ API')

    depends_on('gmsh', when='+examples', type='build')
    depends_on('gmsh', when='+gmsh@4.4.1:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos +kokkos +teuchos', when='+trilinos')
    depends_on('zlib', when='+zlib')

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86610
    conflicts('%gcc@8:8.2.99', when='@:9.22.1')

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
        if '+gmsh' in self.spec:
            args.append('-DOmega_h_USE_Gmsh:BOOL=ON')
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
