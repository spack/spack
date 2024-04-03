# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtBatchai(PythonPackage):
    """Microsoft Azure Batch AI Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-batchai/azure-mgmt-batchai-2.0.0.zip"

    version(
        "2.0.0",
        sha256="b5f7df6a77fde0bd6b486762eb2c81750b6f1730ee1116689d2dfbd3e03dba95",
        url="https://pypi.org/packages/d9/a5/ab796c2a490155c14f9ac4240724ca5c56723315d4dc753030712e6f2e80/azure_mgmt_batchai-2.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:2")
        depends_on("py-msrestazure@0.4.20:", when="@1:2")
