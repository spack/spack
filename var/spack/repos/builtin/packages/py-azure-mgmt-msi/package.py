# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtMsi(PythonPackage):
    """Microsoft Azure MSI Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-msi/azure-mgmt-msi-1.0.0.zip"

    version(
        "1.0.0",
        sha256="e75175af21f9a471c1e8d7a538c11905d65083b86d661b9a759578fb65a1dbcc",
        url="https://pypi.org/packages/34/68/ed34c2646ac06a67df96c31243a50f7af29c14624eff0e8fced137ec6c09/azure_mgmt_msi-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="e989e61753bf4eca0e688526b7c31c9a88082080acfb038fad17dda7f084a026",
        url="https://pypi.org/packages/ae/95/b451721e38ca0feddce03ee3ce86158e208d0150253bd371207a8df4e9c5/azure_mgmt_msi-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:0")
        depends_on("py-msrest@0.5:", when="@1")
        depends_on("py-msrestazure@0.4.32:", when="@1")
        depends_on("py-msrestazure@0.4.27:", when="@0.2:0")
