# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libluv(CMakePackage):
    """This library makes libuv available to lua scripts.
    It was made for the luvit project but should usable from nearly
    any lua project."""

    homepage = "https://github.com/luvit/luv"
    url      = "https://github.com/luvit/luv/releases/download/1.36.0-0/luv-1.36.0-0.tar.gz"

    version('1.43.0-0', sha256='567a6f3dcdcf8a9b54ddc57ffef89d1e950d72832b85ee81c8c83a9d4e0e9de2')
    version('1.42.0-1', sha256='4b6fbaa89d2420edf6070ad9e522993e132bd7eb2540ff754c2b9f1497744db2')
    version('1.42.0-0', sha256='b5228a9d0eaacd9f862b6270c732d5c90773a28ce53b6d9e32a14050e7947f36')
    version('1.36.0-0', sha256='f2e7eb372574f25c6978c1dc74280d22efdcd7df2dda4a286c7fe7dceda26445')

    depends_on('lua-lang', type='link')
    depends_on('libuv', type='link')

    def cmake_args(self):
        args = [
            '-DLUA_BUILD_TYPE=System',
            '-DBUILD_STATIC_LIBS=ON',
            '-DBUILD_SHARED_LIBS=ON',
            '-DWITH_SHARED_LIBUV=ON',
        ]
        return args
