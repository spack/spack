# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningFabric(PythonPackage):
    """Fabric is the fast and lightweight way to scale PyTorch models without boilerplate."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "lightning-fabric/lightning-fabric-2.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.0.0",
        sha256="b006ac4a4f245af41c69963234577db358faf5c14af0e4c3aa6dfffab370425a",
        url="https://pypi.org/packages/57/dc/eb35fb83129da1996ad967880452a0907a21abd5f235a3e94d235dcf9bff/lightning_fabric-2.0.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@2:")
        depends_on("py-fsspec@2021.6.1:+http", when="@1:2.1.2")
        depends_on("py-lightning-utilities@0.7:", when="@2.0.0:2.0")
        depends_on("py-numpy@1.17.2:", when="@1:")
        depends_on("py-packaging@17.1:", when="@1.9.0:2.0")
        depends_on("py-torch@1.11:", when="@2:2.1.0-rc0")
        depends_on("py-typing-extensions@4:", when="@1:2.1")
