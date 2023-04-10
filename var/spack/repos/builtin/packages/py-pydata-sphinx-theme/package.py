# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydataSphinxTheme(PythonPackage):
    """A clean, three-column, Bootstrap-based Sphinx theme by and for the PyData community."""

    homepage = "https://pydata-sphinx-theme.readthedocs.io/en/stable/"
    pypi = "pydata_sphinx_theme/pydata_sphinx_theme-0.9.0.tar.gz"

    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("0.13.3", sha256="827f16b065c4fd97e847c11c108bf632b7f2ff53a3bca3272f63f3f3ff782ecc")

    depends_on("py-sphinx-theme-builder@0.2.0b2", type="build")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-accessible-pygments", type=("build", "run"))
    depends_on("py-babel", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pygments@2.7:", type=("build", "run"))
    depends_on("py-sphinx@4.2:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    conflicts("py-docutils@0.17")
