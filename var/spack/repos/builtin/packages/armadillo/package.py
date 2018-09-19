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


class Armadillo(CMakePackage):
    """Armadillo is a high quality linear algebra library (matrix maths)
    for the C++ language, aiming towards a good balance between speed and
    ease of use."""

    homepage = "http://arma.sourceforge.net/"
    url = "http://sourceforge.net/projects/arma/files/armadillo-7.200.1.tar.xz"

    version('8.100.1', 'd9762d6f097e0451d0cfadfbda295e7c')
    version('7.950.1', 'c06eb38b12cae49cab0ce05f96147147')
    # NOTE: v7.900.1 download url seems broken is no v7.950.1?
    version('7.900.1', '5ef71763bd429a3d481499878351f3be')
    version('7.500.0', '7d316fdf3c3c7ea92b64704180ae315d')
    version('7.200.2', 'b21585372d67a8876117fd515d8cf0a2')
    version('7.200.1', 'ed86d6df0058979e107502e1fe3e469e')

    variant('hdf5', default=False, description='Include HDF5 support')

    depends_on('cmake@2.8.12:', type='build')
    depends_on('arpack-ng')  # old arpack causes undefined symbols
    depends_on('blas')
    depends_on('lapack')
    depends_on('superlu@5.2:')
    depends_on('hdf5', when='+hdf5')

    # Adds an `#undef linux` to prevent preprocessor expansion of include
    # directories with `linux` in them getting transformed into a 1.
    # E.g. `/path/linux-x86_64/dir` -> `/path/1-x86_64/dir` if/when a linux
    # platform's compiler is adding `#define linux 1`.
    patch('undef_linux.patch', when='platform=linux')

    def cmake_args(self):
        spec = self.spec

        return [
            # ARPACK support
            '-DARPACK_LIBRARY={0}'.format(spec['arpack-ng'].libs.joined(";")),
            # BLAS support
            '-DBLAS_LIBRARY={0}'.format(spec['blas'].libs.joined(";")),
            # LAPACK support
            '-DLAPACK_LIBRARY={0}'.format(spec['lapack'].libs.joined(";")),
            # SuperLU support
            '-DSuperLU_INCLUDE_DIR={0}'.format(spec['superlu'].prefix.include),
            '-DSuperLU_LIBRARY={0}'.format(spec['superlu'].libs.joined(";")),
            # HDF5 support
            '-DDETECT_HDF5={0}'.format('ON' if '+hdf5' in spec else 'OFF')
        ]
