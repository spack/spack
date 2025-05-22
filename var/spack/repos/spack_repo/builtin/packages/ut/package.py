# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Ut(CMakePackage):
    """UT: C++20 μ(micro)/Unit Testing Framework"""

    homepage = "https://boost-ext.github.io/ut"
    url = "https://github.com/boost-ext/ut/archive/v0.0.0.tar.gz"
    git = "https://github.com/boost-ext/ut.git"

    maintainers("msimberg")

    license("BSL-1.0")

    version("master", branch="master")
    version("2.3.1", sha256="e51bf1873705819730c3f9d2d397268d1c26128565478e2e65b7d0abb45ea9b1")
    version("2.3.0", sha256="9c07a2b7947cc169fc1713ad462ccc43a704076447893a1fd25bdda5eec4aab6")
    version("2.1.1", sha256="016ac5ece1808cd1100be72f90da4fa59ea41de487587a3283c6c981381cc216")
    version("2.1.0", sha256="1c9c35c039ad3a9795a278447db6da0a4ec1a1d223bf7d64687ad28f673b7ae8")
    version("2.0.1", sha256="1e43be17045a881c95cedc843d72fe9c1e53239b02ed179c1e39e041ebcd7dad")
    version("2.0.0", sha256="8b5b11197d1308dfc1fe20efd6a656e0c833dbec2807e2292967f6e2f7c0420f")
    version("1.1.9", sha256="1a666513157905aa0e53a13fac602b5673dcafb04a869100a85cd3f000c2ed0d")

    depends_on("cxx", type="build")

    generator("ninja")

    depends_on("cmake@3.21:3.25", type="build", when="@master")
    depends_on("cmake@3.12:3.20", type="build", when="@1.1.9")
    depends_on("ninja", type="build")

    conflicts("%gcc@:8")
    conflicts("%clang@:8")
    conflicts("%clang@:10", when="platform=darwin")

    # 1.1.9 had the version set to 1.1.8. See: https://github.com/boost-ext/ut/pull/492.
    patch(
        "https://github.com/boost-ext/ut/commit/67b136c0267a54248d05fcba63905ff5e6abf0b7.patch?full_index=1",
        sha256="0b7ad701a4f9bd6276f7d8b7c464d4ba98cc8c18d436f0eb769c639e67296a69",
        when="@1.1.9",
    )

    def cmake_args(self):
        return [
            self.define("BOOST_UT_BUILD_BENCHMARKS", False),
            self.define("BOOST_UT_BUILD_EXAMPLES", False),
            self.define("BOOST_UT_BUILD_TESTS", self.run_tests),
        ]
