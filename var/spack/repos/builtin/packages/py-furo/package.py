# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme."""

    homepage = "https://www.example.com"
    pypi = "furo/furo-2022.6.21.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("2022.6.21", sha256="9aa983b7488a4601d13113884bfb7254502c8729942e073a0acb87a5512af223")

    depends_on("py-sphinx-theme-builder@0.2.0a10:", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-sphinx@4:", type=("build", "run"))
    depends_on("py-sphinx-basic-ng", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
