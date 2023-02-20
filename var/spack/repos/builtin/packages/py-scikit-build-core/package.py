# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuildCore(PythonPackage):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    homepage = "https://github.com/scikit-build/scikit-build-core"
    pypi = "scikit_build_core/scikit_build_core-0.2.0.tar.gz"
    git = "https://github.com/scikit-build/scikit-build-core"

    maintainers("wdconinc")

    version("0.2.0", sha256="d2a76d9447a412038dc5e25dd259b03c25278661a0c7c3da766bb971c1a9acd2")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-exceptiongroup", when="^python@:3.10", type=("build", "run"))
    depends_on("py-importlib-resources@1.3:", when="^python@:3.8", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="^python@:3.7", type=("build", "run"))

    depends_on("cmake@3.15:", type=("build", "run"))
