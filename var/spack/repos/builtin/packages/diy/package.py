# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diy(CMakePackage):
    """Data-parallel out-of-core library"""

    homepage = "https://github.com/diatomic/diy"
    url = "https://github.com/diatomic/diy/archive/3.6.0.tar.gz"
    git = "https://github.com/diatomic/diy.git"

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("3.6.0", sha256="d12eb7dabe3a8a66cd406d34aabdb43c1ec178b7ed40cf1dff10016643bbf149")
    version("3.5.0", sha256="b3b5490441d521b6e9b33471c782948194bf95c7c3df3eb97bc5cf4530b91576")

    depends_on("mpi")

    def cmake_args(self):
        args = [
            "-Dbuild_examples=off",
            "-Dbuild_tests=off",
            "-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx,
        ]
        return args
