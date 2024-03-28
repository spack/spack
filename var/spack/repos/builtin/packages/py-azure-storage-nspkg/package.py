# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureStorageNspkg(PythonPackage):
    """Microsoft Azure Storage Namespace Package."""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-nspkg/azure-storage-nspkg-3.1.0.tar.gz"

    version(
        "3.1.0",
        sha256="7da3bd6c73b8c464a57f53ae9af8328490d2267c66430d8a7621997e52a9703e",
        url="https://pypi.org/packages/ba/f6/054ace7b01c6c21b3b95a83c3997f7d6539d939a2c08c4f27f779128a030/azure_storage_nspkg-3.1.0-py2.py3-none-any.whl",
    )
