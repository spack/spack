# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Detray(CMakePackage):
    """Detray is a description library for high energy physics experiments that
    works entirely without polymorphism, making it exceptionally suitable for
    use on GPU platforms."""

    homepage = "https://github.com/acts-project/detray"
    url = "https://github.com/acts-project/detray/archive/refs/tags/v0.67.0.tar.gz"

    tags = ["hep"]

    maintainers("stephenswat")

    license("MPL-2.0", checked_by="stephenswat")

    version("0.72.1", sha256="6cc8d34bc0d801338e9ab142c4a9884d19d9c02555dbb56972fab86b98d0f75b")
    version("0.71.0", sha256="2be2b3dac6f77aa8cea033eba841378dc3703ff93c99e4d05ea03df685e6d508")
    version("0.70.0", sha256="14fa1d478d44d5d987caea6f4b365bce870aa8e140c21b802c527afa3a5db869")
    version("0.69.1", sha256="7100ec86a47458a35f5943cd6c7da07c68b8c1c2f62d36d13b8bb50568d0abe5")
    version("0.68.0", sha256="6d57835f22ced9243fbcc29b84ea4c01878a46bfa5910e320c933e9bf8e96612")
    version("0.67.0", sha256="87b1b29f333c955ea6160f9dda89628490d85a9e5186c2f35f57b322bbe27e18")

    variant("csv", default=True, description="Enable the CSV IO plugin")
    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        description="C++ standard used",
    )
    variant("json", default=True, description="Enable the JSON IO plugin")
    variant(
        "scalar",
        default="float",
        values=("float", "double"),
        multi=False,
        description="Scalar type to use by default",
    )
    variant("eigen", default=True, description="Enable the Eigen math plugin")
    variant("smatrix", default=False, description="Enable the SMatrix math plugin")
    variant("vc", default=True, description="Enable the Vc math plugin")

    depends_on("cmake@3.11:", type="build")
    depends_on("vecmem@1.6.0:")
    depends_on("covfie@0.10.0:")
    depends_on("nlohmann-json@3.11.0:", when="+json")
    depends_on("dfelibs@20211029:")
    depends_on("acts-algebra-plugins@0.18.0: +vecmem")
    depends_on("acts-algebra-plugins +vc", when="+vc")
    depends_on("acts-algebra-plugins +eigen", when="+eigen")
    depends_on("acts-algebra-plugins +smatrix", when="+smatrix")

    with when("+smatrix"):
        depends_on("acts-algebra-plugins cxxstd=17", when="cxxstd=17")
        depends_on("acts-algebra-plugins cxxstd=20", when="cxxstd=20")
        depends_on("acts-algebra-plugins cxxstd=23", when="cxxstd=23")

    depends_on("actsvg +meta")

    def cmake_args(self):
        args = [
            self.define("DETRAY_USE_SYSTEM_LIBS", True),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_CUDA_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_SYCL_STANDARD", "cxxstd"),
            self.define_from_variant("DETRAY_CUSTOM_SCALARTYPE", "scalar"),
            self.define_from_variant("DETRAY_EIGEN_PLUGIN", "eigen"),
            self.define_from_variant("DETRAY_SMATRIX_PLUGIN", "smatrix"),
            self.define_from_variant("DETRAY_IO_CSV", "csv"),
            self.define_from_variant("DETRAY_IO_JSON", "json"),
            self.define("DETRAY_SVG_DISPLAY", True),
            self.define("DETRAY_SETUP_ACTSVG", True),
            self.define("DETRAY_BUILD_TESTING", False),
            self.define("DETRAY_SETUP_GOOGLETEST", False),
            self.define("DETRAY_SETUP_BENCHMARK", False),
            self.define("DETRAY_BUILD_TUTORIALS", False),
        ]

        return args
