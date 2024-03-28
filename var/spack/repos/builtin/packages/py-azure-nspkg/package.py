# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureNspkg(PythonPackage):
    """Microsoft Azure Namespace Package [Internal]."""

    homepage = "hhttps://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-nspkg/azure-nspkg-3.0.2.zip"

    version(
        "3.0.2",
        sha256="1d0bbb2157cf57b1bef6c8c8e5b41133957364456c43b0a43599890023cca0a8",
        url="https://pypi.org/packages/c2/95/af354f2f415d250dafe26a5d94230558aa8cf733a9dcbf0d26cd61f5a9b8/azure_nspkg-3.0.2-py2-none-any.whl",
    )
