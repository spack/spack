# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvault(PythonPackage):
    """Microsoft Azure Key Vault Client Libraries for Python."""

    homepage = (
        "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault"
    )
    pypi = "azure-keyvault/azure-keyvault-4.1.0.zip"

    version(
        "4.1.0",
        sha256="5fa0438f7f6e2e79543f2724957acf77c3c187e558f4d030a4f9b7493b9f946d",
        url="https://pypi.org/packages/34/d9/76d295cf6324cc811612710ca5d913015340efb558bdaf5d4a59884958c0/azure_keyvault-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="dec5334cde846849dfe7896f2e98f17b4f4d75c316a4d30e7171ce71ca20713d",
        url="https://pypi.org/packages/80/37/e80f577570b32648c4b88c8c48a46501a4868ae4c8d905774fd02c2b01fc/azure_keyvault-1.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@1")
        depends_on("py-azure-keyvault-certificates@4.1:", when="@4.1")
        depends_on("py-azure-keyvault-keys@4.1:", when="@4.1")
        depends_on("py-azure-keyvault-secrets@4.1:", when="@4.1")
        depends_on("py-azure-nspkg@2:", when="@:0,1.0.0:1")
        depends_on("py-cryptography@2.1.4:", when="@1")
        depends_on("py-msrest@0.5:", when="@1.1:1")
        depends_on("py-msrestazure@0.4.32:", when="@1.1:1")
        depends_on("py-requests@2.18.4:", when="@1")
