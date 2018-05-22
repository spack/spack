#############################################################################
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


class Nektar(CMakePackage):
    """Nektar++: Spectral/hp Element Framework"""

    homepage = "https://www.nektar.info/"
    url      = "https://gitlab.nektar.info/nektar/nektar/-/archive/v4.4.1/nektar-v4.4.1.tar.bz2"

    version('4.4.1', '1be7d061c3cafd9a0f1eb8d281d99b89')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('fftw', default=True, description='Builds with fftw support')
    variant('arpack', default=True, description='Builds with arpack support')
    variant('hdf5', default=True, description='Builds with hdf5 support')
    variant('scotch', default=False,
            description='Builds with scotch partitioning support')

    depends_on('cmake@2.8.8:', type='build', when="~hdf5")
    depends_on('cmake@3.2:', type='build', when="+hdf5")

    depends_on('blas')
    depends_on('lapack')
    depends_on('boost@1.56.0: +iostreams')
    depends_on('tinyxml', when='platform=darwin')

    depends_on('mpi', when='+mpi')
    depends_on('fftw@3.0: +mpi', when="+mpi+fftw")
    depends_on('fftw@3.0: ~mpi', when="~mpi+fftw")
    depends_on('arpack-ng +mpi', when="+arpack+mpi")
    depends_on('arpack-ng ~mpi', when="+arpack~mpi")
    depends_on('hdf5 +mpi +hl', when="+mpi+hdf5")
    depends_on('scotch ~mpi ~metis', when="~mpi+scotch")
    depends_on('scotch +mpi ~metis', when="+mpi+scotch")

    conflicts("+hdf5", when="~mpi",
              msg="Nektar's hdf5 output is for parallel builds only")

    def cmake_args(self):
        args = []

        def hasfeature(feature):
            return 'ON' if feature in self.spec else 'OFF'

        args.append('-DNEKTAR_USE_MPI=%s' % hasfeature('+mpi'))
        args.append('-DNEKTAR_USE_FFTW=%s' % hasfeature('+fftw'))
        args.append('-DNEKTAR_USE_ARPACK=%s' % hasfeature('+arpack'))
        args.append('-DNEKTAR_USE_HDF5=%s' % hasfeature('+hdf5'))
        args.append('-DNEKTAR_USE_SCOTCH=%s' % hasfeature('+scotch'))
        args.append('-DNEKTAR_USE_PETSC=OFF')
        return args
