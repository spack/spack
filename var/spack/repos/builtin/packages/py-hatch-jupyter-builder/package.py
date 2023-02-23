# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchJupyterBuilder(PythonPackage):
    """A hatch plugin to help build Jupyter packages"""

    homepage = "https://github.com/jupyterlab/hatch-jupyter-builder"
    pypi = "hatch-jupyter-builder/hatch_jupyter_builder-0.8.2.tar.gz"

    version("0.8.2", sha256="6436daace48622cefc8585c5d2988a1046c074b65ab5715de04666535a5edff7")

    depends_on("py-hatchling@1.5:", type="build")
    depends_on("python@3.8:", type=("build", "run"))
