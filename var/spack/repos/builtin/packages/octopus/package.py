# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Octopus(Package):
    """A real-space finite-difference (time-dependent) density-functional
    theory code."""

    homepage = "https://octopus-code.org/"
    url      = "http://octopus-code.org/down.php?file=6.0/octopus-6.0.tar.gz"

    version('7.3',   sha256='ad843d49d4beeed63e8b9a2ca6bfb2f4c5a421f13a4f66dc7b02f6d6a5c4d742')
    version('6.0',   sha256='4a802ee86c1e06846aa7fa317bd2216c6170871632c9e03d020d7970a08a8198')
    version('5.0.1', sha256='3423049729e03f25512b1b315d9d62691cd0a6bd2722c7373a61d51bfbee14e0')

    variant('scalapack', default=False,
            description='Compile with Scalapack')
    variant('metis', default=False,
            description='Compile with METIS')
    variant('parmetis', default=False,
            description='Compile with ParMETIS')
    variant('netcdf', default=False,
            description='Compile with Netcdf')
    variant('arpack', default=False,
            description='Compile with ARPACK')

    depends_on('blas')
    depends_on('gsl@1.9:')
    depends_on('lapack')
    depends_on('libxc')
    depends_on('mpi')
    depends_on('fftw@3:+mpi+openmp')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scalapack', when='+scalapack')
    depends_on('netcdf-fortran', when='+netcdf')
    depends_on('arpack-ng', when='+arpack')

    # optional dependencies:
    # TODO: etsf-io, sparskit,
    # feast, libfm, pfft, isf, pnfft

    def install(self, spec, prefix):
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs
        args = []
        args.extend([
            '--prefix=%s' % prefix,
            '--with-blas=%s' % blas.ld_flags,
            '--with-lapack=%s' % lapack.ld_flags,
            '--with-gsl-prefix=%s' % spec['gsl'].prefix,
            '--with-libxc-prefix=%s' % spec['libxc'].prefix,
            'CC=%s' % spec['mpi'].mpicc,
            'FC=%s' % spec['mpi'].mpifc,
            '--enable-mpi',
            '--with-fftw-prefix==%s' % spec['fftw'].prefix,
        ])
        if '+metis' in spec:
            args.extend([
                '--with-metis-prefix=%s' % spec['metis'].prefix,
            ])
        if '+parmetis' in spec:
            args.extend([
                '--with-parmetis-prefix=%s' % spec['parmetis'].prefix,
            ])
        if '+netcdf' in spec:
            args.extend([
                '--with-netcdf-prefix=%s' % spec['netcdf-fortran'].prefix,
                '--with-netcdf-include=%s' %
                spec['netcdf-fortran'].prefix.include,
            ])
        if '+arpack' in spec:
            arpack_libs = spec['arpack-ng'].libs.joined()
            args.extend([
                '--with-arpack={0}'.format(arpack_libs),
            ])
            if '+mpi' in spec['arpack-ng']:
                args.extend([
                    '--with-parpack={0}'.format(arpack_libs),
                ])

        if '+scalapack' in spec:
            args.extend([
                '--with-blacs=%s' % spec['scalapack'].libs,
                '--with-scalapack=%s' % spec['scalapack'].libs
            ])

            # --with-etsf-io-prefix=
            # --with-sparskit=${prefix}/lib/libskit.a
            # --with-pfft-prefix=${prefix} --with-mpifftw-prefix=${prefix}
            # --with-berkeleygw-prefix=${prefix}

        # When preprocessor expands macros (i.e. CFLAGS) defined as quoted
        # strings the result may be > 132 chars and is terminated.
        # This will look to a compiler as an Unterminated character constant
        # and produce Line truncated errors. To vercome this, add flags to
        # let compiler know that the entire line is meaningful.
        # TODO: For the lack of better approach, assume that clang is mixed
        # with GNU fortran.
        if spec.satisfies('%clang') or spec.satisfies('%gcc'):
            args.extend([
                'FCFLAGS=-O2 -ffree-line-length-none'
            ])

        configure(*args)
        make()
        # short tests take forever...
        # make('check-short')
        make('install')
