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


class Fftw(Package):
    """FFTW is a C subroutine library for computing the discrete Fourier
       transform (DFT) in one or more dimensions, of arbitrary input
       size, and of both real and complex data (as well as of even/odd
       data, i.e. the discrete cosine/sine transforms or DCT/DST). We
       believe that FFTW, which is free software, should become the FFT
       library of choice for most applications."""

    homepage = "http://www.fftw.org"
    url      = "http://www.fftw.org/fftw-3.3.4.tar.gz"

    version('3.3.6-pl1', '682a0e78d6966ca37c7446d4ab4cc2a1')
    version('3.3.5', '6cc08a3b9c7ee06fdd5b9eb02e06f569')
    version('3.3.4', '2edab8c06b24feeb3b82bbb3ebf3e7b3')
    version('2.1.5', '8d16a84f3ca02a785ef9eb36249ba433')

    patch('pfft-3.3.5.patch', when="@3.3.5+pfft_patches", level=0)
    patch('pfft-3.3.4.patch', when="@3.3.4+pfft_patches", level=0)

    variant(
        'float', default=True,
        description='Produces a single precision version of the library')
    variant(
        'long_double', default=True,
        description='Produces a long double precision version of the library')
    variant(
        'quad', default=False,
        description='Produces a quad precision version of the library '
                    '(works only with GCC and libquadmath)')
    variant('openmp', default=False, description="Enable OpenMP support.")
    variant('mpi', default=True, description='Activate MPI support')
    variant(
        'pfft_patches', default=False,
        description='Add extra transpose functions for PFFT compatibility')

    depends_on('mpi', when='+mpi')
    depends_on('automake', type='build', when='+pfft_patches')
    depends_on('autoconf', type='build', when='+pfft_patches')

    def install(self, spec, prefix):
        # Base options
        options = [
            '--prefix={0}'.format(prefix),
            '--enable-shared',
            '--enable-threads'
        ]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")
        if spec.satisfies('@:2'):
            options.append('--enable-type-prefix')

        # Variants that affect every precision
        if '+openmp' in spec:
            # Note: Apple's Clang does not support OpenMP.
            if spec.satisfies('%clang'):
                ver = str(self.compiler.version)
                if ver.endswith('-apple'):
                    raise InstallError("Apple's clang does not support OpenMP")
            options.append('--enable-openmp')
            if spec.satisfies('@:2'):
                # TODO: libtool strips CFLAGS, so 2.x libxfftw_threads
                #       isn't linked to the openmp library. Patch Makefile?
                options.insert(0, 'CFLAGS=' + self.compiler.openmp_flag)
        if '+mpi' in spec:
            options.append('--enable-mpi')
        if '+pfft_patches' in spec:
            autoreconf = which('autoreconf')
            autoreconf('-ifv')

        # SIMD support
        # TODO: add support for more architectures
        float_options = []
        double_options = []
        if 'x86_64' in spec.architecture and spec.satisfies('@3:'):
            float_options.append('--enable-sse2')
            double_options.append('--enable-sse2')

        # Build double precision
        configure(*(options + double_options))
        make()
        if self.run_tests:
            make("check")
        make("install")

        # Build float/long double/quad variants
        if '+float' in spec:
            configure('--enable-float', *(options + float_options))
            make()
            if self.run_tests:
                make("check")
            make("install")
        if spec.satisfies('@3:+long_double'):
            configure('--enable-long-double', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
        if spec.satisfies('@3:+quad'):
            configure('--enable-quad-precision', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
