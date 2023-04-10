# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBookTheme(PythonPackage):
    """A clean book theme for scientific explanations and documentation with Sphinx."""

    homepage = "https://sphinx-book-theme.readthedocs.io/"
    pypi = "sphinx_book_theme/sphinx_book_theme-0.3.3.tar.gz"

    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("1.0.1", sha256="927b399a6906be067e49c11ef1a87472f1b1964075c9eea30fb82c64b20aedee")

    depends_on("py-sphinx-theme-builder@0.2.0a7:", type="build")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-pydata-sphinx-theme@0.13.3:", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pygments@2.7:", type=("build", "run"))
    depends_on("py-sphinx@4:6", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    conflicts("py-docutils@0.17")
