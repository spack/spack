# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureKeyvaultNspkg(PythonPackage):
    """Microsoft Azure Key Vault Namespace Package."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault"
    pypi = "azure-keyvault-nspkg/azure-keyvault-nspkg-1.0.0.zip"

    version(
        "1.0.0",
        sha256="04f505c736d899da41e81a873ff2edccca53a4a4b451a77a10083722b8002a70",
        url="https://pypi.org/packages/f2/be/28ff251e315509e7f4b8fa5a5968d72291982a93196752b5b45782af2249/azure_keyvault_nspkg-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-nspkg@3:")
