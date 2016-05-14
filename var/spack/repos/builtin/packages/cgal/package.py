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


class Cgal(Package):
    """
    CGAL is a software project that provides easy access to efficient and reliable geometric algorithms in the form of
    a C++ library. CGAL is used in various areas needing geometric computation, such as geographic information systems,
    computer aided design, molecular biology, medical imaging, computer graphics, and robotics.
    """
    homepage = 'http://www.cgal.org/'
    url = 'https://github.com/CGAL/cgal/archive/releases/CGAL-4.7.tar.gz'

    version('4.7', '4826714810f3b4c65cac96b90fb03b67')
    version('4.6.3', 'e8ee2ecc8d2b09b94a121c09257b576d')

    # Installation instructions : http://doc.cgal.org/latest/Manual/installation.html
    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds a debug version of the libraries')

    depends_on('boost')
    depends_on('mpfr')
    depends_on('gmp')
    depends_on('zlib')
    depends_on('cmake')

    # FIXME : Qt5 dependency missing (needs Qt5 and OpenGL)
    # FIXME : Optional third party libraries missing

    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)
        # CGAL supports only Release and Debug build type. Any other build type will raise an error at configure time
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
