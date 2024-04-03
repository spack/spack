# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepdiff(PythonPackage):
    """Deep Difference and Search of any Python object/data.."""

    homepage = "https://github.com/seperman/deepdiff"
    pypi = "deepdiff/deepdiff-5.6.0.tar.gz"

    license("MIT")

    version(
        "6.3.0",
        sha256="15838bd1cbd046ce15ed0c41e837cd04aff6b3e169c5e06fca69d7aa11615ceb",
        url="https://pypi.org/packages/33/4f/8feec2f9ef4515fc63566ec95a4775afd3ab1f08b563240469aa6afabd41/deepdiff-6.3.0-py3-none-any.whl",
    )
    version(
        "5.6.0",
        sha256="ef3410ca31e059a9d10edfdff552245829835b3ecd03212dc5b533d45a6c3f57",
        url="https://pypi.org/packages/18/d1/25134e24783076814071e51b5417407947398dd4c99e607ec3c9feca5c90/deepdiff-5.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@6:")
        depends_on("py-ordered-set@4.0.2:", when="@6:")
        depends_on("py-ordered-set@4.0.2:4.0", when="@5.2:5.7")
