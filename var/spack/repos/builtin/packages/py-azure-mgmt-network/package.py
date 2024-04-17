# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNetwork(PythonPackage):
    """Microsoft Azure Network Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-network/azure-mgmt-network-11.0.0.zip"

    version(
        "11.0.0",
        sha256="0a4bda7341e33b2cfa567928f4374fe4e0c5710a328174f780813359ef15786b",
        url="https://pypi.org/packages/ed/6f/2f2fa743ec853f20bf151ca139aa4ae3eb3cd6319834a8f780cd634d7716/azure_mgmt_network-11.0.0-py2.py3-none-any.whl",
    )
    version(
        "10.2.0",
        sha256="f82b8b3874e0655a10fb36077036fb3e8e3daa96fa42c964e8b91ef5a466a8e6",
        url="https://pypi.org/packages/39/d8/84a181e6e4926ebad56e68c1d05427f5ad64e7a784acab82a302dc4a93d2/azure_mgmt_network-10.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:18")
        depends_on("py-msrestazure@0.4.32:", when="@:13")
