# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerinstance(PythonPackage):
    """Microsoft Azure Container Instance Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerinstance/azure-mgmt-containerinstance-2.0.0.zip"

    version(
        "2.0.0",
        sha256="1d08587c30d870e2f7961e865dab01db3160f8a8ad53a525d94b0ce7115d39e7",
        url="https://pypi.org/packages/47/89/20bf1f4bb8d54f7f6fb96f0743c3b35871a7fac7dd5273c84c7201ff12c4/azure_mgmt_containerinstance-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="0e55fb1dddcc01a9d58a99095e5cca50252bb6c42150b225e552560fe29fd8a5",
        url="https://pypi.org/packages/fd/d1/d770050f20ad81b80f7eb41f89e1a5d841cf74bf41c7e1ff137c46f28a1e/azure_mgmt_containerinstance-1.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@1.1:7")
        depends_on("py-msrestazure@0.4.32:", when="@1.1:3")
