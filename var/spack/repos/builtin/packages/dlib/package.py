# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Dlib(CMakePackage):
    """toolkit containing machine learning algorithms and tools
    for creating complex software in C++ to solve real world problems"""

    homepage = "http://dlib.net/"
    url = "https://github.com/davisking/dlib/archive/v19.19.tar.gz"
    git = "https://github.com/davisking/dlib"

    maintainer = ["robertu94"]

    version("master", branch="master")
    version("19.22", sha256="5f44b67f762691b92f3e41dcf9c95dd0f4525b59cacb478094e511fdacb5c096")
    version("19.21", sha256="116f52e58be04b47dab52057eaad4b5c4d5c3032d927fe23d55b0741fc4107a0")
    version("19.20", sha256="fc3f0986350e8e53aceadf95a71d2f413f1eedc469abda99a462cb528741d411")
    version("19.19", sha256="7af455bb422d3ae5ef369c51ee64e98fa68c39435b0fa23be2e5d593a3d45b87")

    variant("shared", default=True, description="build the shared libraries")

    depends_on("zlib")
    depends_on("libpng")
    depends_on("libjpeg")
    depends_on("blas")
    depends_on("lapack")
    depends_on("libsm")
    depends_on("libx11")

    def cmake_args(self):
        args = []
        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        return args
