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


class Accfft(CMakePackage, CudaPackage):
    """AccFFT extends existing FFT libraries for CUDA-enabled
    Graphics Processing Units (GPUs) to distributed memory clusters
    """

    homepage = "http://accfft.org"
    git      = "https://github.com/amirgholami/accfft.git"

    version('develop', branch='master')

    variant('pnetcdf', default=True, description='Add support for parallel NetCDF')
    variant('shared', default=True, description='Enables the build of shared libraries')

    # See: http://accfft.org/articles/install/#installing-dependencies
    depends_on('fftw+float+double~mpi+openmp')

    depends_on('parallel-netcdf', when='+pnetcdf')

    parallel = False

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DFFTW_ROOT={0}'.format(spec['fftw'].prefix),
            '-DFFTW_USE_STATIC_LIBS=false',
            '-DBUILD_GPU={0}'.format('true' if '+cuda' in spec else 'false'),
            '-DBUILD_SHARED={0}'.format(
                'true' if '+shared' in spec else 'false'
            ),
        ]

        if '+cuda' in spec:
            cuda_arch = [x for x in spec.variants['cuda_arch'].value if x]
            if cuda_arch:
                args.append('-DCUDA_NVCC_FLAGS={0}'.format(
                    ' '.join(self.cuda_flags(cuda_arch))
                ))

        return args
