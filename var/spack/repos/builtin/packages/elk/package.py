# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elk(MakefilePackage):
    """An all-electron full-potential linearised augmented-plane wave
    (FP-LAPW) code with many advanced features."""

    homepage = 'https://elk.sourceforge.io/'
    url      = 'https://sourceforge.net/projects/elk/files/elk-3.3.17.tgz'

    version('7.2.42', sha256='73f03776dbf9b2147bfcc5b7c062af5befa0944608f6fc4b6a1e590615400fc6')
    version('7.1.14', sha256='7c2ff30f4b1d72d5dc116de9d70761f2c206700c69d85dd82a17a5a6374453d2')
    version('7.0.12', sha256='9995387c681d0e5a9bd52cb274530b23c0370468b6be86f6c90a6ec445cb8a01')
    version('3.3.17', sha256='c9b87ae4ef367ed43afc2d43eb961745668e40670995e8e24c13db41b7e85d73', deprecated=True)

    # what linear algebra packages to use? the choices are
    # internal - use internal libraries
    # generic  - use spack-provided blas and lapack
    # openblas - use openblas specifically, with special support for multithreading.
    # mkl - use mkl specifically, with special support for multithreading
    # should be used with fft=mkl
    # blis - use internal lapack and blas implementation from blis
    variant('linalg', default='internal', multi=False,
            description='Build with custom BLAS library',
            values=('internal', 'generic', 'openblas', 'mkl', 'blis'))
    # what FFT package to use? The choices are
    # internal - use internal library
    # fftw - fftw3 with special code
    # mkl  - use mklr with fft code
    # should be used with linalg=mkls
    variant('fft',    default='internal', multi=False,
            description='Build with custom FFT library',
            values=('internal', 'fftw', 'mkl'))
    #  check that if fft=mkl then linalg=mkl and vice versa.

    conflicts('linalg=mkl', when='fft=fftw')
    conflicts('linalg=mkl', when='fft=internal')
    conflicts('linalg=blis', when='@:3')
    conflicts('fft=mkl', when='linalg=internal')
    conflicts('fft=mkl', when='linalg=generic')
    conflicts('fft=mkl', when='linalg=openblas')
    conflicts('fft=mkl', when='linalg=blis')

    variant('mpi', default=True,
            description='Enable MPI parallelism')
    variant('openmp', default=True,
            description='Enable OpenMP support')
    variant('libxc',  default=True,
            description='Link to Libxc functional library')
    variant('w90', default=False,
            description='wannier90 support, requires wannier90 library')

    depends_on('blas', when='linalg=generic')
    depends_on('lapack', when='linalg=generic')

    depends_on('mkl', when='linalg=mkl')
    depends_on('mkl threads=openmp', when='linalg=mkl +openmp')

    depends_on('openblas', when='linalg=openblas')
    depends_on('openblas threads=openmp', when='linalg=openblas +openmp')

    depends_on('blis', when='linalg=blis')
    depends_on('blis threads=openmp', when='linalg=blis +openmp')

    depends_on('fftw', when='fft=fftw')
    depends_on('fftw +openmp', when='fft=fftw +openmp')
    depends_on('mkl', when='fft=mkl')

    depends_on('mpi@2:', when='+mpi')
    depends_on('libxc@5:', when='@7:+libxc')
    depends_on('libxc@:3', when='@:3+libxc')
    depends_on('wannier90', when='+w90')

    # Cannot be built in parallel
    parallel = False

    def edit(self, spec, prefix):
        # Dictionary of configuration options with default values assigned
        config = {
            'MAKE':      'make',
            'AR':        'ar',
            'LIB_LPK':   'lapack.a blas.a',
            'LIB_FFT':   'fftlib.a',
            'SRC_MPI':   'mpi_stub.f90',
            'SRC_MKL':   'mkl_stub.f90',
            'SRC_OBLAS': 'oblas_stub.f90',
            'SRC_OMP':   'omp_stub.f90',
            'SRC_BLIS':  'blis_stub.f90',
            'SRC_libxc': 'libxcifc_stub.f90',
            'SRC_FFT':   'zfftifc.f90',
            'SRC_W90S':  'w90_stub.f90',
            'F90':        spack_fc,
            'F77':        spack_f77

        }
        # Compiler-specific flags

        flags = ''
        if self.compiler.name == 'intel':
            flags = '-O3 -ip -unroll -no-prec-div'
        elif self.compiler.name == 'gcc':
            flags = '-O3 -ffast-math -funroll-loops'
        elif self.compiler.name == 'pgi':
            flags = '-O3 -lpthread'
        elif self.compiler.name == 'g95':
            flags = '-O3 -fno-second-underscore'
        elif self.compiler.name == 'nag':
            flags = '-O4 -kind=byte -dusty -dcfuns'
        elif self.compiler.name == 'xl':
            flags = '-O3'
        config['F90_OPTS'] = flags
        config['F77_OPTS'] = flags

        if '+mpi' in spec:
            config['F90'] = spec['mpi'].mpifc
            config['F77'] = spec['mpi'].mpif77
            config['SRC_MPI'] = ' '

        # OpenMP support
        if '+openmp' in spec:
            config['F90_OPTS'] += ' ' + self.compiler.openmp_flag
            config['F77_OPTS'] += ' ' + self.compiler.openmp_flag
            config['SRC_OMP'] = ' '

        # BLAS/LAPACK support
        # Note: openblas must be compiled with OpenMP support
        # if the +openmp variant is chosen
        if 'linalg=generic' in spec:
            blas = spec['blas'].libs.joined()
            lapack = spec['lapack'].libs.joined()
            config['LIB_LPK'] = ' '.join([lapack, blas])
        if 'linalg=openblas' in spec:
            config['LIB_LPK']   = spec['openblas'].libs.ld_flags
            config['SRC_OBLAS'] = ' '
        if 'linalg=mkl' in spec:
            config['LIB_LPK']   = spec['mkl'].libs.ld_flags
            config['SRC_MKL']   = ' '
        if 'linalg=blis' in spec:
            config['LIB_LPK']   = ' '.join(['lapack.a ', spec['blis'].libs.ld_flags])
            config['SRC_BLIS']  = ' '
        # FFT
        if 'fft=fftw' in spec:
            config['LIB_FFT'] = spec['fftw'].libs.ld_flags
            config['SRC_FFT'] = 'zfftifc_fftw.f90'
        if 'fftw=mkl' in spec:
            config['LIB_FFT'] = spec['mkl'].libs.ld_flags
            config['SRC_FFT'] = ' '

        # MPI support
        if '+mpi' in spec:
            config['F90'] = spec['mpi'].mpifc
            config['F77'] = spec['mpi'].mpif77
        else:
            config['F90'] = spack_fc
            config['F77'] = spack_f77
            config['SRC_MPI'] = 'mpi_stub.f90'
        # OpenMP support
        if '+openmp' in spec:
            config['F90_OPTS'] += ' ' + self.compiler.openmp_flag
            config['F77_OPTS'] += ' ' + self.compiler.openmp_flag
            config['SRC_OMP'] = ' '

        # Libxc support
        if '+libxc' in spec:
            config['LIB_libxc'] = ' '.join([
                join_path(spec['libxc'].prefix.lib, 'libxcf90.so'),
                join_path(spec['libxc'].prefix.lib, 'libxc.so')
            ])
            if self.spec.satisfies('@7:'):
                config['SRC_libxc'] = 'libxcf90.f90 libxcifc.f90'
            else:
                config['SRC_libxc'] = 'libxc_funcs.f90 libxc.f90 libxcifc.f90'

        # Write configuration options to include file
        with open('make.inc', 'w') as inc:
            for key in config:
                inc.write('{0} = {1}\n'.format(key, config[key]))

    def install(self, spec, prefix):
        # The Elk Makefile does not provide an install target
        mkdir(prefix.bin)

        install('src/elk',                   prefix.bin)
        install('src/eos/eos',               prefix.bin)
        install('src/spacegroup/spacegroup', prefix.bin)

        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('species',  join_path(prefix, 'species'))
