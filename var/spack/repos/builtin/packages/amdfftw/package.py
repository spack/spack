# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.fftw import FftwBase


class Amdfftw(FftwBase):
    """FFTW (AMD Optimized version) is a comprehensive collection of
    fast C routines for computing the Discrete Fourier Transform (DFT)
    and various special cases thereof.

    It is an open-source implementation of the Fast Fourier transform
    algorithm. It can compute transforms of real and complex-values
    arrays of arbitrary size and dimension.
    AMD Optimized FFTW is the optimized FFTW implementation targeted
    for AMD CPUs.
    """

    _name = 'amdfftw'
    homepage = "https://developer.amd.com/amd-aocl/fftw/"
    url = "https://github.com/amd/amd-fftw/archive/2.2.tar.gz"
    git = "https://github.com/amd/amd-fftw.git"

    version('2.2', sha256='de9d777236fb290c335860b458131678f75aa0799c641490c644c843f0e246f8')

    variant(
        'precision', values=any_combination_of(
            'float', 'single', 'double', 'long_double',\
            'quad').prohibit_empty_set().with_default('float,double'),
        description='Build the selected floating-point precision libraries'
    )

    variant('shared', default=True, description='Builds a shared version of the library')
    variant('openmp', default=True, description="Enable OpenMP support.")
    variant('mpi', default=True, description='Activate MPI support')
    variant('debug', default=False, description='Builds a debug version of the library')

    depends_on('mpi', when='+mpi')
    depends_on('texinfo')
    provides('fftw-api@3', when='@2:')

    conflicts('precision=quad', when='%aocc', msg='AOCC clang doesn\'t support quad precision')
    conflicts('+debug', when='%aocc', msg='AOCC clang doesn\'t support debug')
    conflicts('+openmp', when='%apple-clang', msg="Apple's clang does not support OpenMP")
    conflicts('%gcc@:7.2', when="@2.1:", msg="Recommended GCC version above 7.2 for AMDFFTW")

    def configure(self, spec, prefix):
        """Configure function"""
        # Base options
        options = [
            '--prefix={0}'.format(prefix),
            '--enable-amd-opt',
            '--enable-threads'
            ]

        # Check if coimpiler is AOCC
        if spec.satisfies('%aocc'):
            options.append('CC=clang')
            options.append('CXX=clang++')
            options.append('FC=flang')

        if '+shared' in spec:
            options.append('--enable-shared')

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+mpi' in spec:
            options.append('--enable-mpi')
            options.append('--enable-amd-mpifft')

        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        # Specific SIMD support.
        # float and double precisions are supported
        simd_features = ['sse2', 'avx', 'avx2', 'avx512', 'avx-128-fma', 'kcvi', 'vsx', 'neon']
        simd_options = []
        for feature in simd_features:
            msg = '--enable-{0}' if feature in spec.target else '--disable-{0}'
            simd_options.append(msg.format(feature))

        simd_options += ['--enable-fma' if 'fma' in spec.target else '--disable-fma']

        float_simd_features = ['altivec', 'sse']

        #When enabling configure option "--enable-amd-opt", do not use the \
        #configure option "--enable-generic-simd128" or "--enable-generic-simd256".

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            'float': ['--enable-float'],
            'single': ['--enable-float'],
            'double': None,
            'long_double': ['--enable-long-double'],
            'quad': ['--enable-quad-precision']
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable('../configure')
        for precision in self.selected_precisions:

            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            if precision in ('float', 'single', 'double'):
                opts += simd_options

            # float-only acceleration
            if precision in ('float', 'single'):
                for feature in float_simd_features:
                    if feature in spec.target:
                        msg = '--enable-{0}'
                    else:
                        msg = '--disable-{0}'
                    opts.append(msg.format(feature))

            with working_dir(precision, create=True):
                configure(*opts)
