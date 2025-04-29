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
    variant(
        "cxxstd", default="17", values=["14", "17", "20"], multi=False, description="C++ standard"
    )
    variant(
        "stdheaders",
        default=False,
        when="@stable",
        description="Whether to install headers to emulate standard library headers and namespace",
    )

    depends_on("benchmark", when="+benchmarks")
    depends_on("googletest@1.14:1", when="+tests")

    def cmake_args(self):
        args = [
            self.define_from_variant("MDSPAN_ENABLE_TESTS", "tests"),
            self.define_from_variant("MDSPAN_USE_SYSTEM_GTEST", "tests"),
            self.define_from_variant("MDSPAN_ENABLE_BENCHMARKS", "benchmarks"),
            self.define_from_variant("MDSPAN_ENABLE_EXAMPLES", "examples"),
            self.define_from_variant("MDSPAN_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("MDSPAN_INSTALL_STDMODE_HEADERS", "stdheaders"),
        ]

        return args
