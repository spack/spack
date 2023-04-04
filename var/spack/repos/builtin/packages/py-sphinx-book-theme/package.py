# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBookTheme(PythonPackage):
    """An interactive book theme for Sphinx."""

    homepage = "https://pypi.org/project/sphinx-book-theme/"
    pypi = "sphinx_book_theme/sphinx_book_theme-0.3.3.tar.gz"

    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("0.3.3", sha256="0ec36208ff14c6d6bf8aee1f1f8268e0c6e2bfa3cef6e41143312b25275a6217")
