# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDevtestlabs(PythonPackage):
    """Microsoft Azure DevTestLabs Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-devtestlabs/azure-mgmt-devtestlabs-4.0.0.zip"

    version(
        "4.0.0",
        sha256="aada92d62085d4fb96b3ae843821523e40aa13b8fb1b8457a0b4d3d0ce240403",
        url="https://pypi.org/packages/5a/7a/f05bddebd63acc07a2da35e6034ac8c7f50f2511a9e1b17f7189e993648e/azure_mgmt_devtestlabs-4.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@2.2:")
        depends_on("py-msrest@0.5:", when="@3:9")
        depends_on("py-msrestazure@0.4.32:", when="@3:4")
