# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFparser(PythonPackage):
    """
    This project is based upon the Fortran (77..2003) parser
    originally developed by Pearu Peterson for the F2PY project,
    www.f2py.com. It provides a parser for Fortran source code
    implemented purely in Python with minimal dependencies.

    """

    # Links
    homepage = "https://github.com/stfc/fparser"
    git = "https://github.com/stfc/fparser.git"
    pypi = "fparser/fparser-0.1.4.tar.gz"

    # License
    license("BSD-3-Clause")

    # Releases
    version("develop", branch="master")
    version("0.1.4", sha256="00d4f7e9bbd8a9024c3c2f308dd3be9b0eeff3cb852772c9f3cf0c4909dbafd4")
    version("0.1.3", sha256="10ba8b2803632846f6f011278e3810188a078d89afcb4a38bed0cbf10f775736")
    version("0.0.16", sha256="a06389b95a1b9ed12f8141b69c67343da5ba0a29277b2997b02573a93af14e13")
    version("0.0.6", sha256="bf8a419cb528df1bfc24ddd26d63f2ebea6f1e103f1a259d8d3a6c9b1cd53012")
    version("0.0.5", sha256="f3b5b0ac56fd22abed558c0fb0ba4f28edb8de7ef24cfda8ca8996562215822f")

    # Dependencies for latest version
    depends_on("py-setuptools@61:", type="build", when="@0.1.4:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type=("build", "run"), when="@0.1:")
    depends_on("py-setuptools-scm-git-archive", type="build", when="@0.1:")
    depends_on("py-wheel@0.29:", type="build", when="@0.1:")
    depends_on("py-importlib-metadata", type=("build", "run"), when="@0.1:")

    # Historical dependencies
    depends_on("py-setuptools@42:", type="build", when="@0.1:")
    depends_on("py-numpy", type=("build", "run"), when="@:0.0.5")
    depends_on("py-nose", type=("build", "run"), when="@:0.0.7")
    depends_on("py-six", type=("build", "run"), when="@0.0.6:0.0.16")

    # Dependencies only required for tests:
    depends_on("py-pytest@3.3:", type="test")

    # Test
    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        pytest = which("pytest")
        # Limit pystest to search inside the build tree
        with working_dir("src"):
            pytest()
