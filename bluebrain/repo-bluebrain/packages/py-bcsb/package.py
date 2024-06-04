# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcsb(PythonPackage):
    """Backend service for Brayns Circuit Studio."""

    homepage = "https://bbpgitlab.epfl.ch/viz/brayns/braynscircuitstudiobackend"
    git = "ssh://git@bbpgitlab.epfl.ch/viz/brayns/braynscircuitstudiobackend.git"

    version("develop", branch="develop")
    version("2.4.1", tag="v2.4.1")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-websockets@10.3:", type=("build", "run"))
    depends_on("py-libsonata@0.1.23:", type=("build", "run"))
    depends_on("py-psutil@5.9.5:", type=("build", "run"))
    depends_on("py-bluepy@2.5.1:", type=("build", "run"))
