# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtSql(PythonPackage):
    """Microsoft Azure SQL Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-sql/azure-mgmt-sql-0.19.0.zip"

    version(
        "0.19.0",
        sha256="74643efb92a850165a32449fdd38c0b602ecd032a3c5af8a49811df1d435fdfb",
        url="https://pypi.org/packages/fd/6e/470c2a1e7ef38fa2ed94484fddbb7a59db7e17489d03fb2cba46cd7f47f9/azure_mgmt_sql-0.19.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.10:1")
        depends_on("py-msrestazure@0.4.32:", when="@0.10:0")
