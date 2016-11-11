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

    # ---- See "7 CGAL Libraries" at:
    # http://doc.cgal.org/latest/Manual/installation.html

    # The CORE library provides exact arithmetic for geometric computations.
    # See: http://cs.nyu.edu/exact/core_pages/
    #      http://cs.nyu.edu/exact/core_pages/svn-core.html
    variant('core', default=False,
            description='Build the CORE library for algebraic numbers')
    variant('imageio', default=False,
            description='Build utilities to read/write image files')
    variant('demos', default=False,
            description='Build CGAL demos')

    # Essential Third Party Libraries
    depends_on('boost+thread+system')
    depends_on('gmp')
    depends_on('mpfr')

    # Required for CGAL_ImageIO
    # depends_on('opengl', when='+imageio') # not yet in Spack
    depends_on('zlib')

    # Optional to build CGAL_Qt5 (demos)
    # depends_on('opengl', when='+demos')   # not yet in Spack
    depends_on('qt@5:', when='+demos')

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

        options = std_cmake_args + [
            # CGAL supports only Release and Debug build type. Any
            # other build type will raise an error at configure time
            '-DCMAKE_BUILD_TYPE:STRING=%s' %
            ('Debug' if '+debug' in spec else 'Release'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' %
            ('ON' if '+shared' in spec else 'OFF'),
            '-DWITH_CGAL_Core:BOOL=%s' %
            ('YES' if '+core' in spec else 'NO'),
            '-DWITH_CGAL_ImageIO:BOOL=%s' %
            ('YES' if '+imageio' in spec else 'NO'),
            '-DWITH_CGAL_Qt5:BOOL=%s' %
            ('YES' if '+demos' in spec else 'NO')]

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
