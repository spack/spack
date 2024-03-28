# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSignalr(PythonPackage):
    """Microsoft Azure SignalR Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-signalr/azure-mgmt-signalr-0.4.0.zip"

    version(
        "0.4.0",
        sha256="43d2c63c18bbf4a20a4a8d630a2abc44e3d8b920a4354cc38326220f5f8dd839",
        url="https://pypi.org/packages/8a/fe/8c1b54ad985d4062984b81b9f81354e6ac6fe7c323cfbc4803e088bec4f2/azure_mgmt_signalr-0.4.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.1.1:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@0.1.1:0")
