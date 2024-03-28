# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDns(PythonPackage):
    """Microsoft Azure DNS Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-dns/azure-mgmt-dns-3.0.0.zip"

    version(
        "3.0.0",
        sha256="cac173375bee9c23a045340eaf456807edb7fa8f265f3e96c8acf62a7fa5ef41",
        url="https://pypi.org/packages/fd/e4/135d1b7911321576621d51a70a8f28ef027fe0af9eadff44a0b656586cd1/azure_mgmt_dns-3.0.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="5b80546b0f182d7abe90c43025cd5ca7e6605224b4d5b872cca2456667f172ef",
        url="https://pypi.org/packages/c7/d7/0f986a64b06db93cf29b76f9a188f5778eb959624a00ed6aedc335ee58d2/azure_mgmt_dns-2.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@1.2:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@1.0.1:2")
        depends_on("py-msrest@0.5:", when="@2.0.0:8.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@2.0.0:3")
