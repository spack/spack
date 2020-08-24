# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('4.13',  sha256='3e3dd7a64febda58be54c3cbeba329ab6a73b72d4d7647ba4931ecd1fad0e3bc')
    version('4.12', sha256='442ef4fffb2ad6e4141e5a7902993ae6a4e73f7cb641fae1010bb586f6ca5e3f')
    version('4.11',  sha256='27a7762e5430f5392a1fe12a3a4abdfe667605c40224de1c6599f49d66cfbdd2')
    version('4.9.1', sha256='56557da971b5310c2678ffc5def4109266666ff3adc7babbe446797ee2b90cca')
    version('4.9',   sha256='63ac5df71f912f34f2f0f2e54a303578df51f4ec2627db593a65407d791f9039')
    version('4.7',   sha256='50bd0a1cad7a8957b09012f831eebaf7d670e2a3467e8f365ec0c71fa5436369')
    version('4.6.3', sha256='e338027b8767c0a7a6e4fd8679182d1b83b5b1a0da0a1fe4546e7c0ca094fc21')

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
