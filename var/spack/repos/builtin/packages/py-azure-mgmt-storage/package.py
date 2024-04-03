# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtStorage(PythonPackage):
    """Microsoft Azure Storage Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-storage/azure-mgmt-storage-11.1.0.zip"

    version(
        "11.1.0",
        sha256="62a6a8c1c359026ec560856da25221b66b6f1e0a84763a04e863c6e911bc1a5e",
        url="https://pypi.org/packages/60/6c/2f170614e3414e807c8f18a197237a0a54c3cebf770e4cb3b2ef31138f58/azure_mgmt_storage-11.1.0-py2.py3-none-any.whl",
    )
    version(
        "11.0.0",
        sha256="9148e4144919c55323555b787dd2dd9c473651039c5a2b49e95cb9461cdaf9c3",
        url="https://pypi.org/packages/08/64/04619c2c914aac4793ef0cf32e3aba7752ca2464e36c8f247829a0385ae5/azure_mgmt_storage-11.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:17.0")
        depends_on("py-msrestazure@0.4.32:", when="@:11")
