# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBookTheme(PythonPackage):
    """Lightweight Sphinx theme designed to mimic the look-and-feel of an interactive book."""

    homepage = "https://sphinx-book-theme.readthedocs.io/en/latest"
    pypi = "sphinx_book_theme/sphinx_book_theme-1.0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.0.1",
        sha256="d15f8248b3718a9a6be0ba617a32d1591f9fa39c614469bface777ba06a73b75",
        url="https://pypi.org/packages/8e/45/3abe359075154f4d6a8626f4b591a28cc703d7c169cef1f7b87cab1a62f7/sphinx_book_theme-1.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:1.0")
        depends_on("py-pydata-sphinx-theme@0.13.3:", when="@1.0.1:1.0")
        depends_on("py-sphinx@4.0.0:6", when="@1:1.0")
