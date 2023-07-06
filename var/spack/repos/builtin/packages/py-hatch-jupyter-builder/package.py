# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchJupyterBuilder(PythonPackage):
    """A hatch plugin to help build Jupyter packages."""

    homepage = "https://github.com/jupyterlab/hatch-jupyter-builder"
    pypi = "hatch_jupyter_builder/hatch_jupyter_builder-0.8.3.tar.gz"

    version("0.8.3", sha256="0dbd14a8aef6636764f88a8fd1fcc9a91921e5c50356e6aab251782f264ae960")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling@1.5:", type=("build", "run"))
