# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme."""

    homepage = "https://github.com/pradyunsg/furo"
    pypi = "furo/furo-2023.5.20.tar.gz"

    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("2023.5.20", sha256="40e09fa17c6f4b22419d122e933089226dcdb59747b5b6c79363089827dea16f")
    version("2022.6.21", sha256="9aa983b7488a4601d13113884bfb7254502c8729942e073a0acb87a5512af223")

    depends_on("py-sphinx-theme-builder@0.2.0a10:", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-sphinx@4:", when="@:2022", type=("build", "run"))
    depends_on("py-sphinx@6:7", when="@2023:", type=("build", "run"))
    depends_on("py-sphinx-basic-ng", type=("build", "run"))
    depends_on("py-pygments", when="@:2022", type=("build", "run"))
    depends_on("py-pygments@2.7:", when="@2023:", type=("build", "run"))
