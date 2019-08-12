# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vc(CMakePackage):
    """SIMD Vector Classes for C++"""

    homepage = "https://github.com/VcDevel/Vc"
    url      = "https://github.com/VcDevel/Vc/archive/1.3.0.tar.gz"

    version('1.3.0', '77efc1c16691c7925d4b58f9b30cf03b')
    version('1.2.0', 'a5236df286b845d2fee5ef1e4d27549f')
    version('1.1.0', 'e354c1e3ea1d674b6f2af9c6fd230d81')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebug',
                    'RelWithDebInfo', 'MinSizeRel'))
