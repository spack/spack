# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmake(PythonPackage):
    """CMake is an open-source, cross-platform family of tools designed to
    build, test and package software
    """

    homepage = "https://cmake.org"
    git = "https://github.com/scikit-build/cmake-python-distributions.git"
    pypi = "cmake/cmake-3.22.2.tar.gz"

    version("3.25.2", sha256="bcf9f0369743278ec26961542b31ed1610e6f4cfc20c00a3f1c61985abb3b0d2")
    version("3.25.0", sha256="d1658afd3362273782f57697f2fc4637fda1f5798ac64e0f3418a8ba5f6e790f")
    version("3.24.3", sha256="73fa252b21fce1db988beace3e1a2b21f926dd870322d9f37ff04e773b13a12a")
    version("3.24.2", sha256="c62f317b9c9efb8ded26b910b966569ee6df335f21c8017617cd45d985b985c9")
    version("3.24.1", sha256="204a5e26a1e609c2e8e31db3fe16bb016d358fb31d457e08a8525267afe4eb88")
    version("3.24.0", sha256="4b16db74e79a5eb8e2b1a513157a94a20344987ab41acb2e0676fce9baf9c1aa")
    version("3.23.3", sha256="72dbd32dbabf586b3f8148d8cd807a942bdcf0eb5d0178f5826d2221a947aa96")
    version("3.22.6", sha256="4731681ceb0f001d109cf322acb1f3b9896bceb76882979687552972502ec43f")
    version("3.22.5", sha256="4362d75d12d07bdaf1a467e3edefd866a99d97704bbc2464eb5b6c16695c20b9")
    version("3.22.2", sha256="b5bd5eeb488b13cf64ec963800f3d979eaeb90b4382861b86909df503379e219")
    version("3.21.4", sha256="30fa5ed8a5ad66dcd263adb87f3ce3dc2d0ec0ac3958f5becff577e4b62cd065")
    version("3.18.0", sha256="52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b")

    depends_on("ninja", type="build")
    depends_on("py-scikit-build@0.12:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("git", type="build")
    depends_on("cmake@3.22.2", type=("build", "link", "run"), when="@3.22.2")
    depends_on("cmake@3.21.4", type=("build", "link", "run"), when="@3.21.4")
    depends_on("cmake@3.18.0", type=("build", "link", "run"), when="@3.18.0")

    # see:
    #   https://github.com/scikit-build/cmake-python-distributions/issues/227
    #   https://github.com/spack/spack/pull/28760#issuecomment-1029362288
    for v in ["3.22.2", "3.21.4", "3.18.0"]:
        resource(
            name="cmake-src",
            git="https://gitlab.kitware.com/cmake/cmake.git",
            commit="v{0}".format(v),
            when="@{0}".format(v),
            destination="cmake-src",
            placement="cmake-src",
        )

    def install_options(self, spec, prefix):
        return ["-DBUILD_CMAKE_FROM_SOURCE=ON", "-DCMakeProject_SOURCE_DIR=cmake-src"]
