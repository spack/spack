# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAts(PythonPackage):
    """ATS - Automated Testing System - is an open-source, Python-based tool
    for automating the running of tests of an application across a broad range
    of high performance computers."""

    homepage = "https://github.com/LLNL/ATS"
    git = "https://github.com/LLNL/ATS.git"

    maintainers("white238")

    version("main", branch="main")
    version("7.0.105", tag="7.0.105")
    version("7.0.100", tag="7.0.100")
    version("7.0.5", tag="7.0.5")

    # TODO: Add flux variant when Flux functionality works in ATS

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-setuptools", type="build")
