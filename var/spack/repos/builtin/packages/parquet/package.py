# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Parquet(CMakePackage):
    """C++ bindings for the Apache Parquet columnar data format.
    """

    homepage = "https://github.com/apache/parquet-cpp"
    url = "https://github.com/apache/parquet-cpp/archive/apache-parquet-cpp-1.4.0.tar.gz"

    version('1.4.0', '3a3659e65052ef5a76fb88e4922283b9')

    depends_on('arrow')
    depends_on('boost')
    depends_on('cmake@3.2.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('thrift+pic')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'FastDebug', 'Release'))

    def cmake_args(self):
        args = ['-DPARQUET_USE_SSE=OFF', '-DPARQUET_BUILD_TESTS=OFF']
        for dep in ('arrow', 'thrift'):
            args.append("-D{0}_HOME={1}".format(dep.upper(),
                                                self.spec[dep].prefix))
        return args
