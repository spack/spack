# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyComm(PythonPackage):
    """Jupyter Python Comm implementation, for usage in ipykernel, xeus-python etc."""

    homepage = "https://github.com/ipython/comm"
    pypi = "comm/comm-0.1.3.tar.gz"

    version("0.1.3", sha256="a61efa9daffcfbe66fd643ba966f846a624e4e6d6767eda9cf6e993aadaab93e")

    depends_on("py-hatchling@1.10:", type="build")
    depends_on("py-traitlets@5.3:", type=("build", "run"))
