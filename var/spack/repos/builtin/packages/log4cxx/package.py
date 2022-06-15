# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Log4cxx(CMakePackage):
    """A C++ port of Log4j"""

    homepage = "https://logging.apache.org/log4cxx/latest_stable/"
    url      = "https://dlcdn.apache.org/logging/log4cxx/0.12.0/apache-log4cxx-0.12.0.tar.gz"

    maintainers = ['nicmcd']

    version('0.12.1', sha256='7bea5cb477f0e31c838f0e1f4f498cc3b30c2eae74703ddda923e7e8c2268d22')
    version('0.12.0', sha256='bd5b5009ca914c8fa7944b92ea6b4ca6fb7d146f65d526f21bf8b3c6a0520e44')

    variant('cxxstd', default='17', description='C++ standard',
            values=('11', '17'), multi=False)

    depends_on('cmake@3.13:', type='build')

    depends_on('apr-util')
    depends_on('apr')
    depends_on('boost+thread+system', when='cxxstd=11')
    depends_on('zlib')
    depends_on('zip')

    def cmake_args(self):
        return [
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            self.define('BUILD_TESTING', 'off')]
