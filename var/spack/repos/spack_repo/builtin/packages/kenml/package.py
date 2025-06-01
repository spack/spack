# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Kenml(CMakePackage):
    """Faster and Smaller Language Model Queries with KenML"""

    homepage = "https://kheafield.com/code/kenlm/"
    git = "https://github.com/kpu/kenlm.git"

    version("master", branch="master")

    variant("python", default=True, description="Build Python bindings")
    variant("debug", default=False, description="Build with debug flags")

    extends("python", when="+python")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.10:", type="build")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define_from_variant("BUILD_PYTHON_STANDALONE", "python"),
            self.define("KENLM_MAX_ORDER", 6),
        ]

        if self.spec.variants["debug"].value:
            args.append(self.define("CMAKE_BUILD_TYPE", "Debug"))
        else:
            args.append(self.define("CMAKE_BUILD_TYPE", "Release"))

        return args

    def setup_build_environment(self, env):
        env.set("CXXFLAGS", "-fPIC")
