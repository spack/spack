# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureGraphrbac(PythonPackage):
    """Microsoft Azure Graph RBAC Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-graphrbac/azure-graphrbac-0.61.1.zip"

    version(
        "0.61.1",
        sha256="7b4e0f05676acc912f2b33c71c328d9fb2e4dc8e70ebadc9d3de8ab08bf0b175",
        url="https://pypi.org/packages/3e/93/02056aca45162f9fc275d1eaad12a2a07ef92375afb48eabddc4134b8315/azure_graphrbac-0.61.1-py2.py3-none-any.whl",
    )
    version(
        "0.60.0",
        sha256="0b266602dfc631dca13960cc64bac172bf9dea2cccbb1aa13d1631ce76f14d79",
        url="https://pypi.org/packages/bd/11/f78acb88061fbfb3678cb7f2c7d6ad73b69b08bc558aa56246e9ce0d9998/azure_graphrbac-0.60.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@0.31:")
        depends_on("py-msrest@0.5:", when="@0.50:")
        depends_on("py-msrestazure@0.4.32:", when="@0.50:")
