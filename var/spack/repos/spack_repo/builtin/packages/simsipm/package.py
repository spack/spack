# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Simsipm(CMakePackage):
    """SimSiPM is a simple and easy to use C++ library providing a set of
    object-oriented tools with all the functionality needed to describe
    and simulate Silicon PhotonMultipliers (SiPM) sensors."""

    url = "https://github.com/EdoPro98/SimSiPM/archive/refs/tags/v1.2.4.tar.gz"
    homepage = "https://github.com/EdoPro98/SimSiPM/"
    git = "https://github.com/EdoPro98/SimSiPM.git"

    tags = ["hep"]

    maintainers("vvolkl")

    license("MIT")

    version("2.1.0", sha256="e99fcf81f88419c7d7ee6aecec0bbc7a0abc85c5430a4f910a8962d6f5c54e02")
    version("2.0.2", sha256="ba60ed88b54b1b29d089f583dbce93b3272b0b13d47772941339f1503ee3fa48")
    version("1.2.4", sha256="1c633bebb19c490b5e6dfa5ada4a6bc7ec36348237c2626d57843a25af923211")

    variant("python", default=False, description="Build pybind11-based python bindings")
    variant("openmp", default=False, description="Use OpenMP", when="@:1")

    variant(
        "cxxstd",
        default="17",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cxx", type="build")  # generated

    extends("python", when="+python")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="+python", type=("build", "link"))

    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
            self.define_from_variant("SIPM_BUILD_PYTHON", "python"),
            self.define_from_variant("SIPM_ENABLE_OPENMP", "openmp"),
            self.define("SIPM_ENABLE_TEST", self.run_tests),
        ]
        return args
