# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cereal(CMakePackage):
    """cereal is a header-only C++11 serialization library. cereal takes
       arbitrary data types and reversibly turns them into different
       representations, such as compact binary encodings, XML, or
       JSON. cereal was designed to be fast, light-weight, and easy to
       extend - it has no external dependencies and can be easily bundled
       with other code or used standalone.

    """
    homepage = "http://uscilab.github.io/cereal/"
    url      = "https://github.com/USCiLab/cereal/archive/v1.1.2.tar.gz"

    version('1.2.2', '4c56c7b9499dba79404250ef9a040481')
    version('1.2.1', '64476ed74c19068ee543b53ad3992261')
    version('1.2.0', 'e372c9814696481dbdb7d500e1410d2b')
    version('1.1.2', '34d4ad174acbff005c36d4d10e48cbb9')
    version('1.1.1', '0ceff308c38f37d5b5f6df3927451c27')
    version('1.1.0', '9f2d5f72e935c54f4c6d23e954ce699f')
    version('1.0.0', 'd1bacca70a95cec0ddbff68b0871296b')
    version('0.9.1', '8872d4444ff274ce6cd1ed364d0fc0ad')

    patch("Boost.patch")
    patch("Boost2.patch", when="@1.2.2:")
    patch("pointers.patch")

    depends_on('cmake@2.6.2:', type='build')

    def cmake_args(self):
        # Boost is only used for self-tests, which we are not running (yet?)
        return [
            '-DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE',
            '-DSKIP_PORTABILITY_TEST=TRUE',
            '-DJUST_INSTALL_CEREAL=On',
            '-DWITH_WERROR=Off',
        ]
