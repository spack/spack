# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphobjinv(PythonPackage):
    """Sphinx objects.inv Inspection/Manipulation Tool."""

    homepage = "https://github.com/bskinn/sphobjinv"
    pypi = "sphobjinv/sphobjinv-2.3.1.tar.gz"

    version(
        "2.3.1",
        sha256="f3efe68bb0ba6e32cb50df064fe6349b8f94681589b400dea753a2860dd576b5",
        url="https://pypi.org/packages/89/d2/4642eb80e3c5a9a00bf8a2ae5cb9390aadfd2a491f161d26a014afa63c4a/sphobjinv-2.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-attrs@19.2:", when="@2.1:")
        depends_on("py-certifi", when="@2.1-alpha1:")
        depends_on("py-jsonschema@3.0.0:", when="@2.1:")
