# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import llnl.util.lang
from spack import *
from spack.pkg.builtin.fftw import FftwBase


class Amdfftw(FftwBase):
    """AMD Optimized FFTW.

    FFTW is a comprehensive collection of fast C routines for
    computing the Discrete Fourier Transform (DFT) and various special
    cases thereof. It is an open-source implementation of the Fast
    Fourier transform algorithm. It can compute transforms of real and
    complex-values arrays of arbitrary size and dimension.
    AMD Optimized FFTW is the optimized FFTW implementation targeted
    for AMD CPUs.
    """

    _name = 'amdfftw'
    homepage = "https://developer.amd.com/amd-aocl/fftw/"
    url = "https://github.com/amd/amd-fftw/archive/2.2.tar.gz"
    git = "https://github.com/amd/amd-fftw.git"

    version('2.2', sha256='de9d777236fb290c335860b458131678f75aa0799c641490c644c843f0e246f8')
    version('2.1', sha256='b58e063ddc9bb178dbc9914ae863e26ca511011357dd3ddf36fc014f5875d18c')
    version('2.0', sha256='277b43aedbb667eda20611f52772d10c37c26b137bc5ff108554bd5f133a5e58')

    variant(
        'precision', values=any_combination_of(
            'float', 'double', 'long_double', 'quad'
        ).prohibit_empty_set().with_default('float,double'),
        description='Build the selected floating-point precision libraries'
    )
    variant('openmp', default=False, description="Enable OpenMP support.")
    variant('mpi', default=True, description='Activate MPI support')
    variant('enable-single', default=False, description='Enable Single support.')
    variant(
        'pfft_patches', default=False,
        description='Add extra transpose functions for PFFT compatibility')

    depends_on('mpi', when='+mpi')
    depends_on('automake', type='build', when='+pfft_patches')
    depends_on('autoconf', type='build', when='+pfft_patches')
    depends_on('libtool', type='build', when='+pfft_patches')
    depends_on('texinfo')

    # https://github.com/FFTW/fftw3/commit/902d0982522cdf6f0acd60f01f59203824e8e6f3
    conflicts('%gcc@8:8.9999', when="@3.3.7")
    conflicts('precision=long_double', when='@2.1.5',
              msg='Long double precision is not supported in FFTW 2')
    conflicts('precision=quad', when='@2.1.5',
              msg='Quad precision is not supported in FFTW 2')
    conflicts('+openmp', when='%apple-clang', msg="Apple's clang does not support OpenMP")

    provides('fftw-api@2', when='@2.1.5')
    provides('fftw-api@3', when='@3:')

    @property
    def libs(self):

        # Reduce repetitions of entries
        query_parameters = list(llnl.util.lang.dedupe(
            self.spec.last_query.extra_parameters
        ))

        # List of all the suffixes associated with float precisions
        precisions = [
            ('float', 'f'),
            ('double', ''),
            ('long_double', 'l'),
            ('quad', 'q')
        ]

        # Retrieve the correct suffixes, or use double as a default
        suffixes = [v for k, v in precisions if k in query_parameters] or ['']

        # Construct the list of libraries that needs to be found
        libraries = []
        for sfx in suffixes:
            if 'mpi' in query_parameters and '+mpi' in self.spec:
                libraries.append('libfftw3' + sfx + '_mpi')

            if 'openmp' in query_parameters and '+openmp' in self.spec:
                libraries.append('libfftw3' + sfx + '_omp')

            libraries.append('libfftw3' + sfx)

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def patch(self):
        # If fftw/config.h exists in the source tree, it will take precedence
        # over the copy in build dir.  As only the latter has proper config
        # for our build, this is a problem.  See e.g. issue #7372 on github
        if os.path.isfile('fftw/config.h'):
            os.rename('fftw/config.h', 'fftw/config.h.SPACK_RENAMED')

    def autoreconf(self, spec, prefix):
        if '+pfft_patches' in spec:
            autoreconf = which('autoreconf')
            autoreconf('-ifv')

    @property
    def selected_precisions(self):
        """Precisions that have been selected in this build"""
        return self.spec.variants['precision'].value

    def configure(self, spec, prefix):
        # Base options
        options = [
            '--prefix={0}'.format(prefix),
            '--enable-shared',
            '--enable-threads',
	    '--enable-sse2',
            '--enable-avx',
            '--enable-avx2',
            '--enable-mpi',
            '--enable-openmp',
            '--enable-amd-opt'
        ]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")
        if spec.satisfies('@:2'):
            options.append('--enable-type-prefix')

        # Variants that affect every precision
        if '+openmp' in spec:
            options.append('--enable-openmp')
            if spec.satisfies('@:2'):
                # TODO: libtool strips CFLAGS, so 2.x libxfftw_threads
                #       isn't linked to the openmp library. Patch Makefile?
                options.insert(0, 'CFLAGS=' + self.compiler.openmp_flag)
        if '+mpi' in spec:
            options.append('--enable-mpi')

        if '+single' in self.spec:
            options.append("--enable-single")

        # Specific SIMD support.
        # all precisions
        simd_features = ['sse2', 'avx', 'avx2', 'avx512', 'avx-128-fma',
                         'kcvi', 'vsx', 'neon']
        # float only
        float_simd_features = ['altivec', 'sse']

        simd_options = []
        for feature in simd_features:
            msg = '--enable-{0}' if feature in spec.target else '--disable-{0}'
            simd_options.append(msg.format(feature))

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in
                   simd_features + float_simd_features):
            simd_options += [
                '--enable-generic-simd128',
                '--enable-generic-simd256'
            ]

        simd_options += [
            '--enable-fma' if 'fma' in spec.target else '--disable-fma'
        ]

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            'float': ['--enable-float'],
            'double': None,
            'long_double': ['--enable-long-double'],
            'quad': ['--enable-quad-precision']
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable('../configure')
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            # starting from FFTW 3
            if precision in ('float', 'double') and spec.satisfies('@3:'):
                opts += simd_options

            # float-only acceleration
            if precision == 'float':
                for feature in float_simd_features:
                    if feature in spec.target:
                        msg = '--enable-{0}'
                    else:
                        msg = '--disable-{0}'
                    opts.append(msg.format(feature))

            with working_dir(precision, create=True):
                configure(*opts)

    def for_each_precision_make(self, *targets):
        for precision in self.selected_precisions:
            with working_dir(precision):
                make(*targets)

    def build(self, spec, prefix):
        self.for_each_precision_make()

    def check(self):
        self.for_each_precision_make('check')

    def install(self, spec, prefix):
        self.for_each_precision_make('install')
