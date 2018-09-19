##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class RFftwtools(RPackage):
    """Provides a wrapper for several 'FFTW' functions. This package provides
       access to the two-dimensional 'FFT', the multivariate 'FFT', and the
       one-dimensional real to complex 'FFT' using the 'FFTW3' library. The
       package includes the functions fftw() and mvfftw() which are designed
       to mimic the functionality of the R functions fft() and mvfft().
       The 'FFT' functions have a parameter that allows them to not return
       the redundant complex conjugate when the input is real data."""

    homepage = "https://github.com/krahim/fftwtools"
    url      = "https://cran.r-project.org/src/contrib/fftwtools_0.9-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/fftwtools"

    version('0.9-8', '2d1258fbaf0940b57ed61c8d6cd6694d')

    depends_on('fftw')
