# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPeachpy(PythonPackage):
    """Portable Efficient Assembly Codegen in Higher-level Python."""

    homepage = "https://github.com/Maratyszcza/PeachPy"
    git = "https://github.com/Maratyszcza/PeachPy.git"

    version("master", branch="master")

    depends_on("py-setuptools", type="build")
    depends_on("py-opcodes@0.3.13:", type="build")
    depends_on("py-six", type=("build", "run"))
