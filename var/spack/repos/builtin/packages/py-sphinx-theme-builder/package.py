# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxThemeBuilder(PythonPackage):
    """A tool for authoring Sphinx themes with a simple (opinionated) workflow."""

    homepage = "https://sphinx-theme-builder.readthedocs.io/en/latest"
    pypi = "sphinx-theme-builder/sphinx-theme-builder-0.2.0b2.tar.gz"
    git = "https://github.com/pradyunsg/sphinx-theme-builder"

    license("MIT")

    version(
        "0.2.0-beta2",
        sha256="75c7aa71c977aedfca6b368f69d5f5a6e8444222e7716dc927dd8749511147aa",
        url="https://pypi.org/packages/fc/b3/64215aa620ab5d8d00118b378e43b94b8ba01d3640cf1e6bbdb01a7389ab/sphinx_theme_builder-0.2.0b2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2.0-alpha14:")
        depends_on("py-nodeenv")
        depends_on("py-packaging")
        depends_on("py-pyproject-metadata", when="@0.2.0-beta1:")
        depends_on("py-rich")
        depends_on("py-setuptools")
        depends_on("py-tomli", when="@0.2.0-beta2: ^python@:3.10")
        depends_on("py-typing-extensions", when="@0.2.0-alpha15: ^python@:3.6")
