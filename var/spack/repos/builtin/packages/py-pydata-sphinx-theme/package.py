# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydataSphinxTheme(PythonPackage):
    """A clean, three-column, Bootstrap-based Sphinx theme by and for the PyData community."""

    homepage = "https://pydata-sphinx-theme.readthedocs.io/en/stable"
    pypi = "pydata_sphinx_theme/pydata_sphinx_theme-0.14.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.14.1",
        sha256="c436027bc76ae023df4e70517e3baf90cdda5a88ee46b818b5ef0cc3884aba04",
        url="https://pypi.org/packages/81/0d/87e4ca68a348a62a15008ddfb24fc6bb54e060dcc061b87bbf0f801f574a/pydata_sphinx_theme-0.14.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.14")
        depends_on("py-accessible-pygments")
        depends_on("py-babel", when="@0.13.0-rc5:")
        depends_on("py-beautifulsoup4")
        depends_on("py-docutils@:0.17-beta1,0.17.1-beta1:")
        depends_on("py-packaging")
        depends_on("py-pygments@2.7:")
        depends_on("py-sphinx@5.0.0:", when="@0.14:")
        depends_on("py-typing-extensions", when="@0.13.3:")
