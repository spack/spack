# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrayskull(PythonPackage):
    """Project to generate recipes for conda packages."""

    homepage = "https://github.com/conda/grayskull"
    pypi = "grayskull/grayskull-2.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.5.0",
        sha256="81477d18cb1c96de06173337a5fe46eb2e04a793dd1773ec990d3efa2c9f8949",
        url="https://pypi.org/packages/68/3e/bc10142d64e27d66144cd462e1c11325bd1beccdce6dda1810cf86f8dc37/grayskull-2.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:")
        depends_on("py-beautifulsoup4", when="@2:")
        depends_on("py-colorama")
        depends_on("py-conda-souschef@2.2.3:")
        depends_on("py-packaging@21.3:")
        depends_on("py-pip")
        depends_on("py-pkginfo")
        depends_on("py-progressbar2@3.53:")
        depends_on("py-rapidfuzz@3:", when="@2.3.1:")
        depends_on("py-requests")
        depends_on("py-ruamel-yaml@0.16.10:")
        depends_on("py-ruamel-yaml-jinja2")
        depends_on("py-semver@3.0.0:3.0.0.0,3.0.1:", when="@2.3.1:")
        depends_on("py-setuptools@30.3:")
        depends_on("py-stdlib-list")
        depends_on("py-tomli")
        depends_on("py-tomli-w")
