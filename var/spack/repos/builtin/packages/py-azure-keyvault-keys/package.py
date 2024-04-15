# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultKeys(PythonPackage):
    """Microsoft Azure Key Vault Keys Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-keys"
    pypi = "azure-keyvault-keys/azure-keyvault-keys-4.1.0.zip"

    version(
        "4.1.0",
        sha256="baf18c6a4b1724a783531ae222a83a5c4600d7fbb581e4d694f3ee759ef18579",
        url="https://pypi.org/packages/bd/11/2b9f1b1dd59337f844b9f857e1bcd1db87af28f84716b6e44fbd48cffea6/azure_keyvault_keys-4.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-core@1.2.1:", when="@4.0.1:4.2.0-beta1")
        depends_on("py-cryptography@2.1.4:", when="@4.0.0-beta3:")
        depends_on("py-msrest@0.6.0:", when="@4.0.1:4.3")
