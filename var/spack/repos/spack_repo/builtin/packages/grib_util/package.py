# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class GribUtil(CMakePackage):
    """This is a collection of NCEP GRIB related utilities.

    This is related to NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util/archive/refs/tags/v1.2.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("1.5.0", sha256="ae5e02f963f6531650669bbe4aed13b28c419cfb6a7007b0dd1fefbffdea02ff")
    version("1.4.0", sha256="41d17886acee80c595980d2a8d48d094077463d313c5891e9035f530c2c4ab78")
    version("1.3.0", sha256="513612ba9ef9b2e6ceb8e4ed7afc6fc4ef941eae1c721c7ccbb57d7bca0e0d7c")
    version("1.2.4", sha256="f021d6df3186890b0b1781616dabf953581d71db63e7c2913360336985ccaec7")
    version("1.2.3", sha256="b17b08e12360bb8ad01298e615f1b4198e304b0443b6db35fe990a817e648ad5")

    variant("openmp", default=False, description="Use OpenMP multithreading")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    depends_on("jasper@2.0.25:")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("w3emc", when="@1.2.4:")
    requires("^w3emc +extradeps", when="^w3emc@2.10:2.11")
    requires("^w3emc precision=4,d", when="^w3emc@2.10:")
    depends_on("w3emc@2.10:", when="@1.3:")
    depends_on("w3nco", when="@:1.2.3")
    depends_on("g2")
    depends_on("g2@3.5:", when="@1.5:")
    depends_on("g2@3.4.9:", when="@1.4:")
    depends_on("g2@3.4.8:", when="@1.3:")
    depends_on("g2@3.4:", when="@1.2.4:")
    depends_on("g2c@1.8: +utils", when="@1.3:", type="test")
    depends_on("bacio")
    depends_on("bacio@2.4:", when="@1.2.4:")
    requires("^ip precision=d", when="^ip@4.1:")
    depends_on("ip@3.3.3:", when="@1.2.4:")
    depends_on("ip@:3.3.3", when="@:1.2")
    depends_on("sp", when="^ip@:4")
    requires("^sp precision=d", when="^sp@2.4:")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define("BUILD_TESTING", self.run_tests),
            self.define("G2C_COMPARE", self.run_tests),
        ]
        return args

    def patch(self):
        if self.spec.satisfies("@1.4.0 %intel@:20"):
            filter_file("stop iret", "stop 9", "src/grb2index/grb2index.F90")
        if self.spec.satisfies("@:1.5 ^g2@4:"):
            filter_file(
                r"find_package\(g2 ", "find_package(g2c)\nfind_package(g2 ", "CMakeLists.txt"
            )

    def check(self):
        with working_dir(self.build_directory):
            make("test")
