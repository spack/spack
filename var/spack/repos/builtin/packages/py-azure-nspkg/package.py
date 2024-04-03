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
        sha256="31a060caca00ed1ebd369fc7fe01a56768c927e404ebc92268f4d9d636435e28",
        url="https://pypi.org/packages/c4/0c/c562be95a9a2ed52454f598571cf300b1114d0db2aa27f5b8ed3bb9cd0c0/azure_nspkg-3.0.2-py3-none-any.whl",
    )
