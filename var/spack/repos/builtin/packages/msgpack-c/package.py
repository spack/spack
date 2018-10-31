# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MsgpackC(CMakePackage):
    """A small, fast binary interchange format convertible to/from JSON"""
    homepage = "http://www.msgpack.org"
    url      = "https://github.com/msgpack/msgpack-c/archive/cpp-3.0.1.tar.gz"

    version('3.0.1', 'a79f05f0dc5637c161805d6c0e9bfbe7')
    version('1.4.1', 'e2fd3a7419b9bc49e5017fdbefab87e0')

    depends_on('cmake@2.8.12:', type='build')
    depends_on('googletest', type='test')

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_FLAGS=-Wno-implicit-fallthrough",
            "-DCMAKE_C_FLAGS=-Wno-implicit-fallthrough",
            '-DMSGPACK_BUILD_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]
        return args
