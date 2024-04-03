# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSqlvirtualmachine(PythonPackage):
    """Microsoft Azure SQL Virtual Machine Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-sqlvirtualmachine/azure-mgmt-sqlvirtualmachine-0.5.0.zip"

    version(
        "0.5.0",
        sha256="27b2ba9e1d1bde478b714e7809914baad4499d5e87062d7b5bfbc28765238d08",
        url="https://pypi.org/packages/30/c7/eb497b7d67cf04d817c0ebae8e84e5a6bd455338f21618551666dc5d0403/azure_mgmt_sqlvirtualmachine-0.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:0")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
