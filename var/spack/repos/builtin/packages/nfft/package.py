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


class Nfft(AutotoolsPackage):
    """NFFT is a C subroutine library for computing the nonequispaced discrete
    Fourier transform (NDFT) in one or more dimensions, of arbitrary input
    size, and of complex data."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/nfft"
    url = "https://www-user.tu-chemnitz.de/~potts/nfft/download/nfft-3.3.2.tar.gz"

    version('3.3.2', '550737c06f4d6ea6c156800169d8f0d9')

    depends_on('fftw')

    def install(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]

        make("distclean")
        configure(*options)
        make()
        if self.run_tests:
            make("check")
        make("install")

        if '+float' in spec['fftw']:
            make("distclean")
            configure('--enable-float', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
        if '+long_double' in spec['fftw']:
            make("distclean")
            configure('--enable-long-double', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
