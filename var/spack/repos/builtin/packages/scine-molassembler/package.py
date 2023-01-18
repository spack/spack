# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ScineMolassembler(CMakePackage):
    """Chemoinformatics toolkit with support for inorganic molecules."""

    homepage = "https://scine.ethz.ch/download/molassembler"
    url = "https://github.com/qcscine/molassembler/archive/refs/tags/1.2.1.tar.gz"

    version("1.2.1", "c9fea41d383b7f54cf8a3ed4dabebe9e942fe3ef5b47895e3533e8ce42dacd38")

    resource(
        name="dev",
        url="https://github.com/qcscine/development-utils/archive/refs/tags/5.0.1.tar.gz",
        sha256="089ca500fc191e04a968ea166d2fe80178b227bc2e6d3926523fa2eee5f6492d",
        placement="_dev",
    )

    patch(
        "https://raw.githubusercontent.com/conda-forge/scine-molassembler-feedstock/0aa909d/recipe/patches/nlohmann_json.patch",
        level=1,
        sha256="a9afcc42b264620ee24505c1857b8493c2fb632a1d155362ba4519814922a6af",
    )

    variant("python", default=False, description="Build Python extension module")

    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("eigen@3:")
    depends_on("googletest")
    # depends_on("nauty")
    depends_on("nlohmann-json", type="build")
    depends_on("python@3.7:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11", when="+python", type=("build", "run"))
    # depends_on("ringdecomposerlib")
    depends_on("scine-core")
    depends_on("scine-utilities")
    depends_on("scine-utilities+python", when="+python", type=("build", "run"))

    extends("python", when="+python")

    def patch(self):
        os.rmdir("dev")
        os.rename("_dev", "dev")

        filter_file(
            "find_package(pybind11 2.6.2 EXACT QUIET)",
            "find_package(pybind11)",
            "dev/cmake/ImportPybind11.cmake",
        )

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("SCINE_BUILD_TESTS", self.run_tests),
            self.define("SCINE_BUILD_PYTHON_BINDINGS", "+python" in self.spec),
            self.define("SCINE_MARCH", ""),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].prefix.lib),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].prefix.include),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
        if "+python" in self.spec:
            args.append(self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path))
        return args
