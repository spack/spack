# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtAdvisor(PythonPackage):
    """Microsoft Azure Advisor Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-advisor/azure-mgmt-advisor-4.0.0.zip"

    version(
        "4.0.0",
        sha256="ad923ed8d187b67bd7320107a660f4a9bba9c24ad141dc118e434e848cba39cc",
        url="https://pypi.org/packages/8d/96/ce9c9dd989e5b338a9979cc0a62661c36579e6830dbcf08ca0192a698001/azure_mgmt_advisor-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.1",
        sha256="9e424188d71cd35478bff4591eeee2ceb0b097da87f349bc5de5b39799be26de",
        url="https://pypi.org/packages/12/52/5b8ff97a7056fd1d4458677e7628b81bb9c22013ec9a761e39d0e9d55498/azure_mgmt_advisor-2.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@2:9")
        depends_on("py-msrestazure@0.4.32:", when="@2:4")
