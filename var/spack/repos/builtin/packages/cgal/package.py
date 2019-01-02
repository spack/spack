# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cgal(CMakePackage):
    """The Computational Geometry Algorithms Library (CGAL) is a C++ library
    that aims to provide easy access to efficient and reliable algorithms in
    computational geometry. CGAL is used in various areas needing geometric
    computation, such as geographic information systems, computer aided design,
    molecular biology, medical imaging, computer graphics, and robotics.
    """
    homepage = 'http://www.cgal.org/'
    url      = 'https://github.com/CGAL/cgal/releases/download/releases/CGAL-4.11/CGAL-4.11.tar.xz'

    version('4.12', 'b12fd24dedfa889a04abfaea565a88bd')
    version('4.11',  '0e9566046e402f8dc514caef11155864')
    version('4.9.1', '820ef17ffa7ed87af6cc9918a961d966')
    version('4.9',   'ee31343dbc4bf7b5b7501ec1650e9233')
    version('4.7',   '623d91fb2ab0a35049dc6098a0f235cc')
    version('4.6.3', '6953897544d41ffcc63ffe58b32a688f')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

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

    depends_on('cmake@2.8.11:', type='build')

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

    def cmake_args(self):
        # Installation instructions:
        # http://doc.cgal.org/latest/Manual/installation.html
        spec = self.spec

        return [
            '-DBUILD_SHARED_LIBS:BOOL=%s' %
            ('ON' if '+shared' in spec else 'OFF'),
            '-DWITH_CGAL_Core:BOOL=%s' %
            ('YES' if '+core' in spec else 'NO'),
            '-DWITH_CGAL_ImageIO:BOOL=%s' %
            ('YES' if '+imageio' in spec else 'NO'),
            '-DWITH_CGAL_Qt5:BOOL=%s' %
            ('YES' if '+demos' in spec else 'NO'),
        ]
