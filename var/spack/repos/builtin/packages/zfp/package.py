# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zfp(CMakePackage, CudaPackage):
    """zfp is a compressed format for representing multidimensional
       floating-point and integer arrays. zfp provides compressed-array
       classes that support high throughput read and write random access
       to individual array elements. zfp also supports serial and parallel
       (OpenMP and CUDA) compression of whole arrays.
    """

    # Package info
    homepage    = 'https://zfp.llnl.gov'
    url         = 'https://github.com/LLNL/zfp/releases/download/0.5.5/zfp-0.5.5.tar.gz'
    git         = 'https://github.com/LLNL/zfp.git'
    maintainers = ['lindstro', 'GarrettDMorrison']

    # Versions
    version('0.5.5', sha256='fdf7b948bab1f4e5dccfe2c2048fd98c24e417ad8fb8a51ed3463d04147393c5')
    version('0.5.4', sha256='746e17aaa401c67dcffd273d6e6f95c76adfbbd5cf523dcad56d09e9d3b71196')
    version('0.5.3', sha256='a5d2f8e5b47a7c92e2a5775b82cbfb3a76c87d0ac83d25abb4ac10ea75a2856e')
    version('0.5.2', sha256='9c738ec525cc76b4bb80b2b3f7c9f07507eeda3a341470e5942cda97efbe9a4f', url='https://github.com/LLNL/zfp/archive/0.5.2/zfp-0.5.2.tar.gz')
    version('0.5.1', sha256='f255dd1708c9ae4dc6a56dd2614e8b47a10d833c87fd349cbd47545a19c2b779', url='https://github.com/LLNL/zfp/archive/0.5.1/zfp-0.5.1.tar.gz')
    version('develop', branch='develop')

    # Build targets
    variant('utilities', default=True,  description='Build utilities')
    variant('examples',  default=False, description='Build examples')
    variant('tests',     default=True,  description='Build tests')
    variant('shared',    default=True,  description='Build shared libraries')

    # Language bindings
    variant('c',       default=False, description='Enable C bindings')
    variant('python',  default=False, description='Enable Python bindings')
    variant('fortran', default=False, description='Enable Fortran bindings')

    # Execution policies
    variant('openmp', default=False, description='Enable OpenMP execution')
    variant('cuda',   default=False, description='Enable CUDA execution')

    # Advanced options
    variant('bsws', default='64', values=('8', '16', '32', '64'), multi=False,
            description='Bit stream word size: use smaller for finer '
            'rate granularity. Use 8 for H5Z-ZFP filter.')
    variant('strided', default=False,
            description='Enable strided access for progressive zfp streams')
    variant('aligned', default=False,
            description='Enable aligned memory allocation')
    variant('twoway', default=False,
            description='Use two-way skew-associative cache')
    variant('fasthash', default=False,
            description='Use a faster but more collision prone hash function')
    variant('profile', default=False,
            description='Count cache misses')

    # Dependencies
    depends_on('cmake@3.4.0:', type='build')
    depends_on('cuda@7:',      type=('build', 'test', 'run'), when='+cuda')
    depends_on('py-numpy',     type=('build', 'test', 'run'), when='+python')
    depends_on('py-cython',    type='build',                  when='+python')

    def cmake_args(self):
        spec = self.spec

        # Common CMake options for zfp 0.5.1 and later
        args = [
            '-DBUILD_UTILITIES:BOOL={0}'.format(
                'ON' if '+utilities' in spec else 'OFF'),
            '-DBUILD_EXAMPLES:BOOL={0}'.format(
                'ON' if '+examples' in spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DZFP_BIT_STREAM_WORD_SIZE:STRING={0}'.format(
                spec.variants['bsws'].value),
            '-DZFP_WITH_BIT_STREAM_STRIDED:BOOL={0}'.format(
                'ON' if '+strided' in spec else 'OFF'),
            '-DZFP_WITH_ALIGNED_ALLOC:BOOL={0}'.format(
                'ON' if '+aligned' in spec else 'OFF'),
            '-DZFP_WITH_CACHE_TWOWAY:BOOL={0}'.format(
                'ON' if '+twoway' in spec else 'OFF'),
            '-DZFP_WITH_CACHE_TWOWAY:BOOL={0}'.format(
                'ON' if '+twoway' in spec else 'OFF')
        ]

        # cfp compressed-array C bindings
        if '+c' in spec:
            if not spec.satisfies('@0.5.4:'):
                raise InstallError('+c requires zfp 0.5.4 or later')
            args.append('-DBUILD_CFP:BOOL=ON')
        else:
            args.append('-DBUILD_CFP:BOOL=OFF')

        # zfPy Python bindings to libzfp
        if '+python' in spec:
            if not spec.satisfies('@0.5.5:'):
                raise InstallError('+python requires zfp 0.5.5 or later')
            args.append('-DBUILD_ZFPY:BOOL=ON')
        else:
            args.append('-DBUILD_ZFPY:BOOL=OFF')

        # zFORp Fortran bindings to libzfp
        if '+fortran' in spec:
            if not spec.satisfies('@0.5.5:'):
                raise InstallError('+fortran requires zfp 0.5.5 or later')
            args.append('-DBUILD_ZFORP:BOOL=ON')
        else:
            args.append('-DBUILD_ZFORP:BOOL=OFF')

        # OpenMP support
        if '+openmp' in spec:
            if not spec.satisfies('@0.5.3:'):
                raise InstallError('+openmp requires zfp 0.5.3 or later')
            args.append('-DZFP_WITH_OPENMP:BOOL=ON')
        else:
            args.append('-DZFP_WITH_OPENMP:BOOL=OFF')

        # CUDA support
        if '+cuda' in spec:
            if not spec.satisfies('@0.5.4:'):
                raise InstallError('+cuda requires zfp 0.5.4 or later')
            args.append('-DZFP_WITH_CUDA:BOOL=ON')
        else:
            args.append('-DZFP_WITH_CUDA:BOOL=OFF')

        # Advanced option: cache fast hash function
        if '+fasthash' in spec:
            if not spec.satisfies('@0.5.2:'):
                raise InstallError('+fasthash requires zfp 0.5.2 or later')
            args.append('-DZFP_WITH_CACHE_FAST_HASH:BOOL=ON')
        else:
            args.append('-DZFP_WITH_CACHE_FAST_HASH:BOOL=OFF')

        # Advanced option: cache profiling
        if '+profile' in spec:
            if not spec.satisfies('@0.5.2:'):
                raise InstallError('+profile requires zfp 0.5.2 or later')
            args.append('-DZFP_WITH_CACHE_PROFILE:BOOL=ON')
        else:
            args.append('-DZFP_WITH_CACHE_PROFILE:BOOL=OFF')

        return args
