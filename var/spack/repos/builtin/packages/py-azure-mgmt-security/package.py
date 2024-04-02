# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSecurity(PythonPackage):
    """Microsoft Azure Security Center Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-security/azure-mgmt-security-0.4.1.zip"

    version(
        "0.4.1",
        sha256="bcc2be82f73b678a85a62b9b4bf1f8427c0b4e0a26d30a3f49ee58943b354d41",
        url="https://pypi.org/packages/ea/54/94085786921076169e05abda8ff63fbd69b783e20abaacb42013dbc8646f/azure_mgmt_security-0.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
