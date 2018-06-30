##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Casacore(CMakePackage):
    """A suite of c++ libraries for radio astronomy data processing."""

    homepage = "https://github.com/casacore/casacore"
    url      = "https://github.com/casacore/casacore/archive/v2.4.1.tar.gz"

    version('2.4.1', '88fdbdadbc1320290c36f1605d3bd9e7')

    variant('openmp', default=False, description='Build OpenMP support')
    variant('shared', default=True, description='Build shared libraries')
    variant('sofa', default=False, description='Build SOFA support')
    variant('fftw', default=False, description='Build FFTW3 support')
    variant('hdf5', default=False, description='Build HDF5 support')
    variant('python', default=False, description='Build python support')
    variant('ncurses', default=False, description='Build ncurses support')

    depends_on('flex')
    depends_on('bison')
    depends_on('blas')
    depends_on('lapack')
    depends_on('cfitsio@3.181:')
    depends_on('wcslib@4.20:')
    depends_on('fftw@3.0.0:', when='+fftw')
    depends_on('sofa-c', when='+sofa')
    depends_on('hdf5', when='+hdf5')
    depends_on('ncurses', when='+ncurses')
    depends_on('python@2.6:', when='+python')
    depends_on('boost+python', when='+python')
    depends_on('py-numpy', when='+python')

    def cmake_args(self):
        args = []
        spec = self.spec

        if '+shared' in spec:
            args.append('-DENABLE_SHARED=YES')
        else:
            args.append('-DENABLE_SHARED=NO')

        if '+openmp' in spec:
            args.append('-DUSE_OPENMP=YES')
        else:
            args.append('-DUSE_OPENMP=NO')

        if '+hdf5' in spec:
            args.append('-DUSE_HDF5=YES')
        else:
            args.append('-DUSE_HDF5=NO')

        if '+fftw' in spec:
            args.append('-DUSE_FFTW3=YES')
        else:
            args.append('-DUSE_FFTW3=NO')

        # Python2 and Python3 binding
        if('+python' not in spec):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=NO'])
        elif(spec['python'].version >= Version('3.0.0')):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=YES'])
        else:
            args.extend(['-DBUILD_PYTHON=YES', '-DBUILD_PYTHON3=NO'])

        return args
