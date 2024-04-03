# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRecoveryservices(PythonPackage):
    """Microsoft Azure Recovery Services Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-recoveryservices/azure-mgmt-recoveryservices-0.5.0.zip"

    version(
        "0.5.0",
        sha256="d65ac640d08531371a1f4f731aec6d1f68b0d6fc77e46ee2a6ee84ff293f893c",
        url="https://pypi.org/packages/48/ee/b35787a3099608eea5b83fff5b46e9b22f3112d8463042bb8b79ab60b365/azure_mgmt_recoveryservices-0.5.0-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="b10fc686ec4ac4a84923458b743755f83e5ad025f52728314293315012a76f35",
        url="https://pypi.org/packages/86/32/941ceae2e22e9b0116e4aa5a11b5547b400ff9d5a95188996fd300de9426/azure_mgmt_recoveryservices-0.4.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.4:1")
        depends_on("py-msrestazure@0.4.32:", when="@0.4:0")
