# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpuinfo(CMakePackage):
    """cpuinfo is a library to detect essential
    for performance optimization information about host CPU."""

    homepage = "https://github.com/pytorch/cpuinfo"
    git = "https://github.com/pytorch/cpuinfo.git"

    version("main", branch="main")
    version("2022-08-19", commit="8ec7bd91ad0470e61cf38f618cc1f270dede599c")  # py-torch@1.13
    version("2020-12-17", commit="5916273f79a21551890fd3d56fc5375a78d1598d")  # py-torch@1.8:1.12
    version("2020-06-11", commit="63b254577ed77a8004a9be6ac707f3dccc4e1fd9")  # py-torch@1.6:1.7
    version("2020-01-21", commit="0e6bde92b343c5fbcfe34ecd41abf9515d54b4a7")  # py-torch@1.5
    version("2019-01-17", commit="89fe1695edf9ee14c22f815f24bac45577a4f135")  # py-torch@1.0.1:1.4
    version("2018-10-05", commit="c342292afb040c868849bc15e96ab894dceba2bc")  # py-torch@1.0.0
    version("2018-05-13", commit="1e6c8c99d27f2b5eb9d2e6231055c6a4115b85e5")  # py-torch@0.4.1
    version("2018-04-04", commit="831dc28341b5f20d13e840caf87eaba644d82643")  # py-torch@:0.4.0

    depends_on("cmake@3.5:", type="build")
    depends_on("ninja", type="build")

    # No option to use pre-installed deps
    # https://github.com/pytorch/cpuinfo/issues/5
    resource(
        name="googlebenchmark",
        url="https://github.com/google/benchmark/archive/v1.6.1.zip",
        sha256="367e963b8620080aff8c831e24751852cffd1f74ea40f25d9cc1b667a9dd5e45",
        destination="deps",
        placement="googlebenchmark",
    )
    resource(
        name="googletest",
        url="https://github.com/google/googletest/archive/release-1.11.0.zip",
        sha256="353571c2440176ded91c2de6d6cd88ddd41401d14692ec1f99e35d013feda55a",
        destination="deps",
        placement="googletest",
    )

    generator = "Ninja"

    def cmake_args(self):
        return [
            self.define("BUILD_SHARED_LIBS", True),
            self.define(
                "GOOGLEBENCHMARK_SOURCE_DIR",
                join_path(self.stage.source_path, "deps", "googlebenchmark"),
            ),
            self.define(
                "GOOGLETEST_SOURCE_DIR", join_path(self.stage.source_path, "deps", "googletest")
            ),
            self.define("CPUINFO_BUILD_UNIT_TESTS", self.run_tests),
            self.define("CPUINFO_BUILD_MOCK_TESTS", self.run_tests),
            self.define("CPUINFO_BUILD_BENCHMARKS", self.run_tests),
        ]
