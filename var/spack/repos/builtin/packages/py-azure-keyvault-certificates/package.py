# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultCertificates(PythonPackage):
    """Microsoft Azure Key Vault Certificates Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-certificates"
    pypi = "azure-keyvault-certificates/azure-keyvault-certificates-4.1.0.zip"

    version(
        "4.1.0",
        sha256="763f4db3cfa4e1ae86d05812276fa50c6d67269eb77926b8367c09c669f5df79",
        url="https://pypi.org/packages/4c/98/d557642c6a2f610475edae7a772eeffcfb4bf02f690994e2fba502176fab/azure_keyvault_certificates-4.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-core@1.2.1:", when="@4.0.1:4.2.0-beta1")
        depends_on("py-msrest@0.6.0:", when="@4.0.0-beta6:4.2")
