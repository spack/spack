# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCosmos(PythonPackage):
    """Microsoft Azure Cosmos Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-cosmos/azure-cosmos-4.0.0.zip"

    license("MIT")

    version(
        "4.0.0",
        sha256="2dbcb33e091b6c3284026472cf3fc3d3ca3cc8bfdc200d469dbd9089f8ba0e54",
        url="https://pypi.org/packages/af/42/f9df4e1cba74ee5058782ef838b0f6caa0c271670e054c263d69702884e2/azure_cosmos-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="313e766bcf5a1779802c274dec94d5b9cc0e4d0d269489c56606fd2464070fad",
        url="https://pypi.org/packages/4a/4f/23ffc8e870df94ea6def08121245301e763eaee7236fb8c3d02d5ff66687/azure_cosmos-3.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-core@1.0.0:", when="@4.0.0-beta5:4.3.0-beta1")
        depends_on("py-requests@2.10:", when="@:3.1.1,3.2:4.0.0-alpha2")
        depends_on("py-six@1.6:", when="@:3.1.1,3.2:4.2")
