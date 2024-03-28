# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatalakeStore(PythonPackage):
    """Microsoft Azure Data Lake Store Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datalake-store/azure-mgmt-datalake-store-0.5.0.zip"

    version(
        "0.5.0",
        sha256="2af98236cd7eaa439b239bf761338c866996ce82e9c129b204e8851e5dc095dd",
        url="https://pypi.org/packages/ff/ac/5685cd06dc8b245bb6b894815764a14bd62245ba4579b45148682f510fdd/azure_mgmt_datalake_store-0.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@0.3:")
        depends_on("py-azure-mgmt-datalake-nspkg@2:", when="@0.1.4:0")
        depends_on("py-msrestazure@0.4.27:", when="@0.5:0")
