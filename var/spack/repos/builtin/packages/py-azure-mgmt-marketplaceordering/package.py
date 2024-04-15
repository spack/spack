# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtMarketplaceordering(PythonPackage):
    """Microsoft Azure Market Place Ordering Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-marketplaceordering/azure-mgmt-marketplaceordering-0.2.1.zip"

    version(
        "0.2.1",
        sha256="12d595f3dbda90de7cbc08ace99b925124ce675219b32bb3fde90e36d357c095",
        url="https://pypi.org/packages/38/10/7a334338d33d5d0f409ee3736568761cf681f2db50a32e477f287c7e4602/azure_mgmt_marketplaceordering-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.2:1.1")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:0")
