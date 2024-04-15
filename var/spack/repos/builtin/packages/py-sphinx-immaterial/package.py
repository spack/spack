# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxImmaterial(PythonPackage):
    """An adaptation of the popular mkdocs-material theme for the Sphinx documentation tool."""

    homepage = "https://github.com/jbms/sphinx-immaterial"
    pypi = "sphinx_immaterial/sphinx_immaterial-0.11.2.tar.gz"

    license("MIT")

    version(
        "0.11.2",
        sha256="96fc25386863a20626827104217b58ec1c541c9d77fc14c169226619fdb2fd9e",
        url="https://pypi.org/packages/13/17/0b7805cd078a47d0fd24faa4fa350b21568ea59f345b06574059ad794375/sphinx_immaterial-0.11.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.11.1:")
        depends_on("py-appdirs", when="@0.9:")
        depends_on("py-markupsafe")
        depends_on("py-pydantic", when="@:0.11.4")
        depends_on("py-requests", when="@0.9:")
        depends_on("py-sphinx@4.0.0:", when="@:0.11.2")
        depends_on("py-typing-extensions")
