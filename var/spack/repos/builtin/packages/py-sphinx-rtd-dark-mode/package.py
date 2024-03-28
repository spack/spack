# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdDarkMode(PythonPackage):
    """A Sphinx extension for adding a toggleable dark mode to the Read the Docs theme."""

    homepage = "https://github.com/MrDogeBro/sphinx_rtd_dark_mode"
    pypi = "sphinx-rtd-dark-mode/sphinx_rtd_dark_mode-1.2.4.tar.gz"

    license("MIT")

    version(
        "1.2.4",
        sha256="1d97c1e4f7902fb77ae86adcf72926c3b0e48a300f93eeba49266da5aeed8a29",
        url="https://pypi.org/packages/2e/b4/3594412eca5b84eb40ceb84ff0f582b91b71ade05a1a7f8bb8e5b23e7897/sphinx_rtd_dark_mode-1.2.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx-rtd-theme")
