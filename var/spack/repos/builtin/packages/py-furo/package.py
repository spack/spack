# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme.."""

    homepage = "https://github.com/pradyunsg/furo"
    pypi = "furo/furo-2023.5.20.tar.gz"

    license("MIT")

    version(
        "2023.9.10",
        sha256="513092538537dc5c596691da06e3c370714ec99bc438680edc1debffb73e5bfc",
        url="https://pypi.org/packages/17/b7/fd357a7961875637930d138aa2667e6fd08bd888a5c173d4b7b2667f7cb9/furo-2023.9.10-py3-none-any.whl",
    )
    version(
        "2023.5.20",
        sha256="594a8436ddfe0c071f3a9e9a209c314a219d8341f3f1af33fdf7c69544fab9e6",
        url="https://pypi.org/packages/fd/7e/4b38c29717b8c1e2d9e839afeb1a133178fd572df176b1c2ee0f159fa5a9/furo-2023.5.20-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2023.8.19:")
        depends_on("python@3.7:", when="@2022.6:2023.8.17")
        depends_on("py-beautifulsoup4")
        depends_on("py-pygments@2.7:", when="@2022.9:")
        depends_on("py-sphinx@6.0.0:", when="@2023.5:")
        depends_on("py-sphinx-basic-ng", when="@2022.6:")
