# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultSecrets(PythonPackage):
    """Microsoft Azure Key Vault Secrets Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets"
    pypi = "azure-keyvault-secrets/azure-keyvault-secrets-4.1.0.zip"

    version(
        "4.1.0",
        sha256="743a2eabb2bbb21d50b46fa6b321361b9b61121387ec35c0f3d953778793c179",
        url="https://pypi.org/packages/6e/66/dc763e4ad80ea059d2a3df55fab8fbfb9ce39f79c0fd38f9c469d05bdbea/azure_keyvault_secrets-4.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-core@1.2.1:", when="@4.0.1:4.2.0-beta1")
        depends_on("py-msrest@0.6.0:", when="@4.0.1:4.2")
