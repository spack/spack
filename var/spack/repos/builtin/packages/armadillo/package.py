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


class Armadillo(Package):
    """Armadillo is a high quality linear algebra library (matrix maths)
    for the C++ language, aiming towards a good balance between speed and
    ease of use."""

    homepage = "http://arma.sourceforge.net/"
    url = "http://sourceforge.net/projects/arma/files/armadillo-7.200.1.tar.xz"

    version('7.200.1', 'ed86d6df0058979e107502e1fe3e469e')

    variant('hdf5', default=False, description='Include HDF5 support')

    depends_on('arpack')
    depends_on('blas')
    depends_on('lapack')
    depends_on('superlu@5.2:')
    depends_on('hdf5', when='+hdf5')

    def install(self, spec, prefix):
        cmake_args = [
            # ARPACK support
            '-DARPACK_LIBRARY={0}/libarpack.a'.format(
                spec['arpack'].prefix.lib),
            # BLAS support
            '-DBLAS_LIBRARY={0}'.format(spec['blas'].blas_shared_lib),
            # LAPACK support
            '-DLAPACK_LIBRARY={0}'.format(spec['lapack'].lapack_shared_lib),
            # SuperLU support
            '-DSuperLU_INCLUDE_DIR={0}'.format(spec['superlu'].prefix.include),
            '-DSuperLU_LIBRARY={0}/libsuperlu.a'.format(
                spec['superlu'].prefix.lib64),
            # HDF5 support
            '-DDETECT_HDF5={0}'.format('ON' if '+hdf5' in spec else 'OFF')
        ]

        cmake_args.extend(std_cmake_args)
        cmake('.', *cmake_args)

        make()
        make('install')
