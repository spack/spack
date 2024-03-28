# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDeploymentmanager(PythonPackage):
    """Microsoft Azure Deployment Manager Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-deploymentmanager/azure-mgmt-deploymentmanager-0.2.0.zip"

    version(
        "0.2.0",
        sha256="1c181936c45ba5e368f6bda97fef3b2630785a31f57b11ca57d6331a2eb23878",
        url="https://pypi.org/packages/2a/57/6be4eb45ded32fe71c99bd4c3fc4a790b032ada6882208de10c636488fa0/azure_mgmt_deploymentmanager-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
