# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtPolicyinsights(PythonPackage):
    """Microsoft Azure Policy Insights Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-policyinsights/azure-mgmt-policyinsights-0.5.0.zip"

    version(
        "0.5.0",
        sha256="30975b18bbd1cda17b88d019fe6168a33619b88583da8b9f0a8b4d5439f7e842",
        url="https://pypi.org/packages/13/72/3592e0e30f4cc0ebbc675fef569e724b2f88372762b84c026d54508b4723/azure_mgmt_policyinsights-0.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.2:1.0")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:0")
