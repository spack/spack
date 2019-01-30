# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gflags(CMakePackage):
    """The gflags package contains a C++ library that implements
    commandline flags processing. It includes built-in support for
    standard types such as string and the ability to define flags
    in the source file in which they are used. Online documentation
    available at: https://gflags.github.io/gflags/"""

    homepage = "https://gflags.github.io/gflags"
    url      = "https://github.com/gflags/gflags/archive/v2.1.2.tar.gz"

    version('2.1.2', 'ac432de923f9de1e9780b5254884599f')

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        return ['-DBUILD_SHARED_LIBS=ON']
