# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openvkl(CMakePackage):
    """
    Intel® Open Volume Kernel Library (Intel Open VKL) is a
    collection of high-performance volume computation kernels,
    developed at Intel.
    """

    homepage = "https://www.openvkl.org"
    git = "https://github.com/openvkl/openvkl.git"
    generator = "Ninja"

    version("1.2.0", tag="v1.2.0")

    depends_on("cmake@3.1:", type="build")
    depends_on("ispc", type="build")
    depends_on("ninja", type="build")
    depends_on("embree")
    depends_on("rkcommon")

    def cmake_args(self):
        return ['-DBUILD_EXAMPLES=OFF']
