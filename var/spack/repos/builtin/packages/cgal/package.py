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
    """The Computational Geometry Algorithms Library (CGAL) is a C++ library
    that aims to provide easy access to efficient and reliable algorithms in
    computational geometry. CGAL is used in various areas needing geometric
    computation, such as geographic information systems, computer aided design,
    molecular biology, medical imaging, computer graphics, and robotics.
    """
    homepage = 'http://www.cgal.org/'
    url = 'https://github.com/CGAL/cgal/archive/releases/CGAL-4.7.tar.gz'

    version('4.9', '7b628db3e5614347f776c046b7666089')
    version('4.7', '4826714810f3b4c65cac96b90fb03b67')
    version('4.6.3', 'e8ee2ecc8d2b09b94a121c09257b576d')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('debug', default=False,
            description='Builds a debug version of the libraries')

    # Essential Third Party Libraries
    depends_on('boost')
    depends_on('gmp')
    depends_on('mpfr')
    depends_on('zlib')
    # depends_on('opengl')
    depends_on('qt@5:')

    # Optional Third Party Libraries
    # depends_on('leda')
    # depends_on('mpfi')
    # depends_on('rs')
    # depends_on('rs3')
    # depends_on('ntl')
    # depends_on('eigen')
    # depends_on('libqglviewer')
    # depends_on('esbtl')
    # depends_on('intel-tbb')

    # Build dependencies
    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        # Installation instructions:
        # http://doc.cgal.org/latest/Manual/installation.html

        options = []
        options.extend(std_cmake_args)

        # CGAL supports only Release and Debug build type. Any other build type
        # will raise an error at configure time
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
