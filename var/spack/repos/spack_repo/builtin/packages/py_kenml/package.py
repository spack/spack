# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyKenml(CMakePackage, PythonPackage):
    """Faster and Smaller Language Model Queries with KenML"""

    homepage = "https://kheafield.com/code/kenlm/"
    git = "https://github.com/kpu/kenlm.git"

    version("master", branch="master")

    variant("python", default=True, description="Build Python bindings")
    depends_on("python", type=("build", "run"), when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("wheel", type="build", when="+python")
    depends_on("cmake@3.10:", type="build")

    variant("debug", default=False, description="Build with debug flags")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BUILD_PYTHON_STANDALONE", True),
            self.define("KENLM_MAX_ORDER", 6),
        ]

        if self.spec.variants["debug"].value:
            args.append(self.define("CMAKE_BUILD_TYPE", "Debug"))
        else:
            args.append(self.define("CMAKE_BUILD_TYPE", "Release"))

        return args

    def setup_build_environment(self, env):
        env.set("CXXFLAGS", "-fPIC")
