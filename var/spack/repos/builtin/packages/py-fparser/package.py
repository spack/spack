# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFparser(PythonPackage):
    """Parser for Fortran 77..2003 code."""

    homepage = "https://github.com/stfc/fparser"
    git = "https://github.com/stfc/fparser.git"
    pypi = "fparser/fparser-0.0.16.tar.gz"

    version("develop", branch="master")
    version("0.0.16", sha256="a06389b95a1b9ed12f8141b69c67343da5ba0a29277b2997b02573a93af14e13")
    version("0.0.6", sha256="bf8a419cb528df1bfc24ddd26d63f2ebea6f1e103f1a259d8d3a6c9b1cd53012")
    version("0.0.5", sha256="f3b5b0ac56fd22abed558c0fb0ba4f28edb8de7ef24cfda8ca8996562215822f")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"), when="@:0.0.5")
    depends_on("py-nose", type=("build", "run"), when="@:0.0.7")
    # six is unused as of 0.0.15, but still listed in setup.py
    depends_on("py-six", type=("build", "run"), when="@0.0.6:")

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Ensure that pytest.ini exists inside the source tree,
        # otherwise an external pytest.ini can cause havoc:
        touch("pytest.ini")
        with working_dir("src"):
            Executable("py.test")()
