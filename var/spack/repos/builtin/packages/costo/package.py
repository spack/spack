# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Costo(CMakePackage):
    """Cosimulation Tools"""

    homepage = "https://gitlab.com/Te_ch/costo"
    git = "https://gitlab.com/Te_ch/costo.git"

    maintainers("tech-91")

    license("LGPL-3.0-or-later")

    version(
        "0.0.5", tag="v0.0.5", commit="6660d69a099fbb874385c0bac1f7e1cfed5111cc", preferred=True
    )
    version("develop", branch="devel")
    version("main", branch="main", deprecated=True)

    variant("shared", default=True, description="Build shared library")
    variant("tests", default=False, description="Enable testing")

    depends_on("mpi", type=all)
    depends_on("python@3.10:", type=all)

    depends_on("py-non-regression-test-tools", type="build")
    depends_on("py-pyvista", type="run")
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-mpi4py", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-mgmetis", type="run")
    depends_on("py-colorama", type="run")
    depends_on("py-pip", type="build")

    def cmake_args(self):
        args = [
            # self.define("COSTO_ENABLE_TESTS", "OFF"),
            self.define("COSTO_ENABLE_PYTHON_BINDINGS", "OFF"),
            self.define("WITH_PYTHON_MODULE", "ON"),
            self.define_from_variant("WITH_SHARED_LIBS", "shared"),
            self.define_from_variant("WITH_TESTS", "tests"),
        ]

        return args
