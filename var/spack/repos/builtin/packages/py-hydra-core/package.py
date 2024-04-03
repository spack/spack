# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHydraCore(PythonPackage):
    """A framework for elegantly configuring complex applications."""

    homepage = "https://github.com/facebookresearch/hydra"
    pypi = "hydra-core/hydra-core-1.3.1.tar.gz"

    license("MIT")

    version(
        "1.3.1",
        sha256="d1c8b273eba0be68218c4ff1ae9a7df7430ce4aa580f1bbebc03297029761cf4",
        url="https://pypi.org/packages/01/d1/d2e852afd72da2ca7f5ee1e71124ef61328282482b1cd8d96d37145bb947/hydra_core-1.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-antlr4-python3-runtime@4.9", when="@1.2:1.2.0.0,1.3:")
        depends_on("py-importlib-resources", when="@1.2: ^python@:3.8")
        depends_on("py-omegaconf@2.2:2.2.0.0,2.2.1:2.3", when="@1.3.1:")
        depends_on("py-packaging", when="@1.2:")
