# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioRmetric(CMakePackage):
    """LibPressio metric that runs R code"""

    url = "https://github.com/robertu94/libpressio-rmetric/archive/refs/tags/0.0.2.tar.gz"
    git = "https://github.com/robertu94/libpressio-rmetric"
    homepage = git

    maintainers("robertu94")

    version("master", branch="master")
    # note versions <= 0.0.3 do not build with spack
    version("0.0.6", sha256="b23a79448cd32b51a7301d6cebf4e228289712dd77dd76d86821741467e9af46")
    version("0.0.5", sha256="51eb192314ef083790dd0779864cab527845bd8de699b3a33cd065c248eae24c")
    version("0.0.4", sha256="166af5e84d7156c828a3f0dcc5bf531793ea4ec44bbf468184fbab96e1f0a91f")
    version("0.0.3", sha256="c45948f83854c87748c7ec828ca2f06d7cf6f98a34f763b68c13a4e2deb7fd79")

    depends_on("libpressio@0.88.0:", when="@0.0.5:")
    depends_on("libpressio@0.85.0:", when="@:0.0.4")
    depends_on("r")
    depends_on("r-rcpp")
    depends_on("r-rinside")

    def cmake_args(self):
        args = []
        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def test(self):
        make("test")
