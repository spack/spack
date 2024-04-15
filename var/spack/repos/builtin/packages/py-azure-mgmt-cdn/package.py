# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCdn(PythonPackage):
    """Microsoft Azure CDN Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-cdn/azure-mgmt-cdn-4.0.0.zip"

    # Release candidate needed for py-azure-cli
    version(
        "4.1.0-rc1",
        sha256="94664a693a72cdaca40101f562f8e1c4a1f9f981f62d7ebc8d2531f196ae24ae",
        url="https://pypi.org/packages/fe/aa/760a4bc961ca766c4bda2f8cfa97169f2c9273e4979d68b4fe73d0205e2c/azure_mgmt_cdn-4.1.0rc1-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="db2bb06ab147125f3f29685811b2ba97e52aafbf926471d26f8f8719e2e7b136",
        url="https://pypi.org/packages/92/91/69f891c427504e9c0914f970b6163141639e71d0e3c4b3d19ded5d728ba7/azure_mgmt_cdn-4.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@2:")
        depends_on("py-msrest@0.5:", when="@3.1:11")
        depends_on("py-msrestazure@0.4.32:", when="@3.1:7")
