# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCmakeParser(PythonPackage):
    """Parse CMake files with Python."""

    homepage = "https://github.com/roehling/cmake_parser"
    pypi = "cmake-parser/cmake_parser-0.9.2.tar.gz"
    git = "https://github.com/roehling/cmake_parser.git"

    maintainers("cmelone")

    license("Apache-2.0", checked_by="cmelone")

    version("0.9.2", sha256="b7a313d3f41e58c09e0886f2c98f3fcee2b1897fe7f87449823a53e51ab23a3d")
    version("main", branch="main")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@61:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    # removed in the main branch in 599f691 but no new pypi release yet
    depends_on("py-attrs@21.3.0:", when="@0.9.2", type=("build", "run"))
