# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylon(PythonPackage):
    """Virus assembler from amplicon sequencing reads."""

    homepage = "https://github.com/iqbal-lab-org/cylon"

    url = "https://github.com/iqbal-lab-org/cylon/archive/refs/tags/v0.1.0.tar.gz"
    git = "https://github.com/iqbal-lab-org/cylon"

    version("main", branch="main")
    version("0.1.0", sha256="4c61c5b600df9c64fb2c323b48642f185ff2cdc8b7b52f06c9827683899501eb")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("racon", type="run")
    depends_on("minimap2", type=("build", "run"))
    depends_on("py-pysam")
    depends_on("py-pyfastaq")
