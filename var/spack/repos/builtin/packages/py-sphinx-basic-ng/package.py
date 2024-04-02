# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxBasicNg(PythonPackage):
    """A modern skeleton for Sphinx themes."""

    homepage = "https://github.com/pradyunsg/sphinx-basic-ng"
    pypi = "sphinx_basic_ng/sphinx_basic_ng-1.0.0b2.tar.gz"

    license("MIT")

    version(
        "1.0.0-beta2",
        sha256="eb09aedbabfb650607e9b4b68c9d240b90b1e1be221d6ad71d61c52e29f7932b",
        url="https://pypi.org/packages/3c/dd/018ce05c532a22007ac58d4f45232514cd9d6dd0ee1dc374e309db830983/sphinx_basic_ng-1.0.0b2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.0.1-alpha11:")
        depends_on("py-sphinx@4.0.0:", when="@1:")
