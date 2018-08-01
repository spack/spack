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


class Typhonio(CMakePackage):
    """TyphonIO is a library of routines that perform input/output (I/O)
        of scientific data within application codes"""

    homepage = "http://uk-mac.github.io/typhonio/"
    url      = "https://github.com/UK-MAC/typhonio/archive/v1.6_CMake.tar.gz"
    git      = "https://github.com/UK-MAC/typhonio.git"

    version('develop', branch='cmake_build')
    version('1.6_CMake', '8e8b2940a57874205e6d451856db5c2755884bf9')

    variant('build_type', default='Release', description='The build type to build',
        values=('Debug', 'Release'))
    variant('fortran', default=False, description='Enable Fortran support')
    variant('shared', default=False, description='Build shared libraries')
    variant('doc', default=False, description='Build user guide and doxygen documentation')

    depends_on('mpi')
    depends_on('hdf5+hl')

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "+fortran" in spec:
            cmake_args.append("-DBUILD_FORTRAN_LIBRARY=ON")
        if "+shared" in spec:
            cmake_args.append("-DBUILD_TIO_SHARED=ON")
        if "+docs" in spec:
            cmake_args.append("-DBUILD_DOXYGEN_DOCS=ON")
            cmake_args.append("-DBUILD_USER_GUIDE=ON")

        return cmake_args
