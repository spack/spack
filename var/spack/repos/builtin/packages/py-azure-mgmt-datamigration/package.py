# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatamigration(PythonPackage):
    """Microsoft Azure Data Migration Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datamigration/azure-mgmt-datamigration-4.0.0.zip"

    version(
        "4.0.0",
        sha256="12c4d1ec735067b82595930373093c9116a579887febfa74d91a7b0e962e885e",
        url="https://pypi.org/packages/d8/53/ba3c95c42febd45d0eb6a0a14e3fa82b3be7547e27da74dd083019e0f195/azure_mgmt_datamigration-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="b58c5b8d2ab92b9f8660dc4a0c2ae74a6415c7b0d01732b0bcc1872323f0be3c",
        url="https://pypi.org/packages/a6/68/aba86e698f24f25f70d9ee2b15a2ca0d71b822932ace8ba96e5beb12efdd/azure_mgmt_datamigration-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:2.0")
        depends_on("py-msrest@0.5:", when="@2:9.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@2:4")
        depends_on("py-msrestazure@0.4.27:", when="@:1")
