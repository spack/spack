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


class Nektar(CMakePackage):
    """Nektar++: Spectral/hp Element Framework"""

    homepage = "https://www.nektar.info/"
    url      = "https://gitlab.nektar.info/nektar/nektar/-/archive/v4.4.1/nektar-v4.4.1.tar.bz2"

    version('4.4.1', '1be7d061c3cafd9a0f1eb8d281d99b89')
    version('4.4.0', 'd4cd211eb7c1fb39915a76645c6e4377')
    version('4.3.5', 'c98089d35a0b9a11462882d086842902')
    version('4.3.4', '9bb27b5ae7b30381728aeacf89875472')
    version('4.3.3', '31cdddf396913331d071a35fdd987d5c')
    version('4.3.2', '28d0fb774658fd6c274e440ac4208748')
    version('4.3.1', 'cabae08c4a646d7a357ddcb6f8559944')
    version('4.3.0', '80dc0f3cb01a36e1a688bcc6d1cec561')
    version('4.2.0', 'fee3df0e000a7257af1e9a83d5c461b3')
    version('4.1.0', 'a2dc4e37849d96261b5107abdff3a088')
    version('4.0.1', 'fcfc7b2771bfa310342b44f363782313')
    version('4.0.0', '9a70068d4122781539bd7e3047a0eb2b')
    version('3.4.0', '72d43a48e8c9b0085bcb025e4fc377e2')
    version('3.3.0', '7b4aecd4dc4c8b1097d9626d684cecd0')
    version('3.2.0', 'ba72e702a10b51fbcc5ed96b4fcfed67')
    version('3.1.0', '1d03860ebdbdcdc1affad47897a398d9')
    version('3.0.1', 'fb6d5a02f5c0bea62d611d2d29447c08')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('fftw', default=True, description='Builds with fftw support')
    variant('arpack', default=True, description='Builds with arpack support')
    variant('hdf5', default=True, description='Builds with hdf5 support')
    variant('scotch', default=False,
            description='Builds with scotch partitioning support')

    depends_on('cmake@2.8.8:', type='build', when="-hdf5")
    depends_on('cmake@3.2:', type='build', when="+hdf5")

    depends_on('blas')
    depends_on('lapack')
    depends_on('boost@1.52.0: +iostreams')
    depends_on('tinyxml', when='platform=darwin')

    depends_on('mpi', when='+mpi')
    depends_on('fftw@3.0: +mpi', when="+mpi+fftw")
    depends_on('fftw@3.0: -mpi', when="-mpi+fftw")
    depends_on('arpack-ng +mpi', when="+arpack+mpi")
    depends_on('arpack-ng ~mpi', when="+arpack~mpi")
    depends_on('hdf5 +mpi +hl', when="+mpi+hdf5")
    depends_on('scotch -mpi -metis', when="-mpi+scotch")
    depends_on('scotch +mpi -metis', when="+mpi+scotch")

    conflicts("+hdf5", when="-mpi")

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
