# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScinePuffin(PythonPackage):
    """Calculation handler for SCINE Chemoton"""

    homepage = "https://scine.ethz.ch/download/puffin"
    pypi = "scine_puffin/scine_puffin-1.1.0.tar.gz"

    version("1.1.0", "1a15232b1b472c36349e5534e4fdf9dd90bc554926cb42fba37eee8e60be8c44")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-gitpython", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-psutil", type="run")
    depends_on("py-python-daemon", type="run")
    depends_on("py-pyyaml", type="run")
    depends_on("py-scine-database", type="run")
    depends_on("py-scine-molassembler", type="run")
    depends_on("py-scine-readuct", type="run")
    depends_on("py-scine-utilities", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-setproctitle", type="run")
    depends_on("py-setuptools", type="build")
