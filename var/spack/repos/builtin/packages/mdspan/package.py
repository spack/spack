# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mdspan(CMakePackage):
    """Extension of std::span to enable multidimensional arrays"""

    homepage = "https://github.com/kokkos/mdspan/tree/stable"
    url = "https://github.com/kokkos/mdspan/archive/refs/tags/mdspan-0.6.0.zip"
    git = "https://github.com/kokkos/mdspan.git"

    maintainers("tpadioleau", "nmm0")

    version("stable", branch="stable")
    version("0.6.0", sha256="d6b7b9d4f472106df1d28729bd8383a8a7ea7938adf9f82d3be9c151344830d9")

    variant("examples", default=True, description="Enable examples")
    variant("tests", default=False, description="Enable tests")
    variant("benchmarks", default=False, description="Enable benchmarks")

    depends_on("benchmark", when="+benchmarks")
    depends_on("googletest@main", when="+tests")

    def cmake_args(self):
        args = [
            self.define_from_variant("MDSPAN_ENABLE_TESTS", "tests"),
            self.define_from_variant("MDSPAN_USE_SYSTEM_GTEST", "tests"),
            self.define_from_variant("MDSPAN_ENABLE_BENCHMARKS", "benchmarks"),
            self.define_from_variant("MDSPAN_ENABLE_EXAMPLES", "examples"),
        ]

        args.append("-DCMAKE_CXX_STANDARD=17")
        args.append("-DMDSPAN_CXX_STANDARD=17")

        return args
