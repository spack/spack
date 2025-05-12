# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Covfie(CMakePackage, CudaPackage, ROCmPackage):
    """Covfie is a library for compositional descriptions of storage methods for
    vector fields and other structured multi-dimensional data."""

    homepage = "https://github.com/acts-project/covfie"
    url = "https://github.com/acts-project/covfie/archive/refs/tags/v0.13.0.tar.gz"
    git = "https://github.com/acts-project/covfie.git"
    list_url = "https://github.com/acts-project/covfie/tags"

    maintainers("stephenswat", "sethrj")

    license("MPL-2.0")

    version("main", branch="main")
    version("0.14.0", sha256="b4d8afa712c6fc0e2bc6474367d65fad652864b18d0255c5f2c18fd4c6943993")
    version("0.13.0", sha256="e9cd0546c7bc9539f440273bbad303c97215ccd87403cedb4aa387a313938d57")
    version("0.12.1", sha256="c33d7707ee30ab5fa8df686a780600343760701023ac0b23355627e1f2f044de")
    version("0.12.0", sha256="e35e94075a40e89c4691ff373e3061577295d583a2546c682b2d652d9fce7828")
    version("0.11.0", sha256="39fcd0f218d3b4f3aacc6af497a8cda8767511efae7a72b47781f10fd4340f4f")
    version("0.10.0", sha256="d44142b302ffc193ad2229f1d2cc6d8d720dd9da8c37989ada4f23018f86c964")

    depends_on("c", type="build", when="@:0.13")
    depends_on("cxx", type="build")

    depends_on("cmake@3.21:", type="build", when="@0.11:")
    depends_on("cmake@3.18:", type="build")

    def cmake_args(self):
        args = [
            self.define("COVFIE_PLATFORM_CPU", True),
            self.define_from_variant("COVFIE_PLATFORM_CUDA", "cuda"),
            self.define_from_variant("COVFIE_PLATFORM_HIP", "rocm"),
            self.define("COVFIE_QUIET", True),
            self.define("COVFIE_BUILD_TESTS", self.run_tests),
        ]

        return args
