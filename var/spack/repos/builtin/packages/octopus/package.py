##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Octopus(Package):
    """A real-space finite-difference (time-dependent) density-functional
    theory code."""

    homepage = "http://www.tddft.org/programs/octopus/"
    base_url = "http://www.tddft.org/programs/octopus/down.php?file="

    version('6.0', '5d1168c2a8d7fd9cb9492eaebaa7182e')
    version('5.0.1', '2b6392ab67b843f9d4ca7413fc07e822')

    # Sample url is:
    # "http://www.tddft.org/programs/octopus/down.php?file=5.0.1/octopus-5.0.1.tar.gz"
    def url_for_version(self, version):
        return '{0}/{1}/octopus-{1}.tar.gz'.format(Octopus.base_url,
                                                   version.dotted)

    variant('scalapack', default=False,
            description='Compile with Scalapack')
    variant('metis', default=True,
            description='Compile with METIS')
    variant('parmetis', default=False,
            description='Compile with ParMETIS')
    variant('netcdf', default=False,
            description='Compile with Netcdf')
    variant('arpack-ng', default=False,
            description='Compile with ARPACK-ng')

    depends_on('blas')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('libxc')
    depends_on('mpi')
    depends_on('fftw+mpi')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scalapack', when='+scalapack')
    depends_on('netcdf-fortran', when='+netcdf')
    depends_on('arpack-ng', when='+arpack-ng')

    # optional dependencies:
    # TODO: parmetis, etsf-io, sparskit,
    # feast, libfm, pfft, isf, pnfft

    def install(self, spec, prefix):
        arpack = find_libraries('libarpack', root=spec[
                                'arpack-ng'].prefix.lib, shared=True)
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
            '--with-fft-lib=-L%s -lfftw3' % spec['fftw'].prefix.lib,
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
        if '+arpack-ng' in spec:
            args.extend([
                '--with-arpack={0}'.format(arpack.joined()),
            ])
        if '+scalapack' in spec:
            args.extend([
                '--with-blacs=%s' % spec['scalapack'].libs,
                '--with-scalapack=%s' % spec['scalapack'].libs,
            ])
            # --with-etsf-io-prefix=
            # --with-sparskit=${prefix}/lib/libskit.a
            # --with-pfft-prefix=${prefix} --with-mpifftw-prefix=${prefix}
            # --with-parpack=${prefix}/lib/libparpack.dylib
            # --with-parmetis-prefix=${prefix}
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
